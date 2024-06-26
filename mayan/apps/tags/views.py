import logging

from django.shortcuts import reverse
from django.template import RequestContext
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.databases.classes import ModelQueryFields
from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.views.document_views import DocumentListView
from mayan.apps.views.generics import (
    MultipleObjectDeleteView, MultipleObjectFormActionView,
    SingleObjectCreateView, SingleObjectEditView, SingleObjectListView
)
from mayan.apps.views.view_mixins import ExternalObjectViewMixin

from .forms import TagForm, TagMultipleSelectionForm
from .icons import (
    icon_document_tag_list, icon_document_tag_multiple_attach,
    icon_document_tag_multiple_remove, icon_menu_tags, icon_tag_create,
    icon_tag_document_list, icon_tag_edit, icon_tag_list,
    icon_tag_single_delete
)
from .links import link_document_tag_multiple_attach, link_tag_create
from .models import DocumentTag, Tag
from .permissions import (
    permission_tag_attach, permission_tag_create, permission_tag_delete,
    permission_tag_edit, permission_tag_remove, permission_tag_view
)

logger = logging.getLogger(name=__name__)


class TagAttachActionView(MultipleObjectFormActionView):
    form_class = TagMultipleSelectionForm
    object_permission = permission_tag_attach
    pk_url_kwarg = 'document_id'
    source_queryset = Document.valid.all()
    success_message_plural = _(
        message='Tags attached to %(count)d documents successfully.'
    )
    success_message_single = _(
        message='Tags attached to document "%(object)s" successfully.'
    )
    success_message_singular = _(
        message='Tags attached to %(count)d document successfully.'
    )
    title_plural = _(message='Attach tags to %(count)d documents.')
    title_single = _(message='Attach tags to document: %(object)s')
    title_singular = _(message='Attach tags to %(count)d document.')
    view_icon = icon_document_tag_multiple_attach

    def get_extra_context(self):
        context = {}

        if self.object_list.count() == 1:
            context.update(
                {
                    'object': self.object_list.first()
                }
            )

        return context

    def get_form_extra_kwargs(self):
        kwargs = {
            'help_text': _(message='Tags to be attached.'),
            'permission': permission_tag_attach,
            'queryset': Tag.objects.all(),
            'user': self.request.user
        }

        if self.object_list.count() == 1:
            kwargs.update(
                {
                    'queryset': Tag.objects.exclude(
                        pk__in=self.object_list.first().tags.all()
                    )
                }
            )

        return kwargs

    def get_post_action_redirect(self):
        if self.object_list.count() == 1:
            return reverse(
                kwargs={
                    'document_id': self.object_list.first().pk
                }, viewname='tags:document_tag_list'
            )
        else:
            return super().get_post_action_redirect()

    def object_action(self, form, instance):
        for tag in form.cleaned_data['tags']:
            AccessControlList.objects.check_access(
                obj=tag, permission=permission_tag_attach,
                user=self.request.user
            )

            tag.attach_to(document=instance, user=self.request.user)


class TagCreateView(SingleObjectCreateView):
    extra_context = {
        'title': _(message='Create tag')
    }
    form_class = TagForm
    post_action_redirect = reverse_lazy(viewname='tags:tag_list')
    view_icon = icon_tag_create
    view_permission = permission_tag_create

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}


class TagDeleteView(MultipleObjectDeleteView):
    error_message = _(
        message='Error deleting tag "%(instance)s"; %(exception)s'
    )
    model = Tag
    object_permission = permission_tag_delete
    pk_url_kwarg = 'tag_id'
    post_action_redirect = reverse_lazy(viewname='tags:tag_list')
    success_message_plural = _(message='%(count)d tags deleted successfully.')
    success_message_single = _(
        message='Tag "%(object)s" deleted successfully.'
    )
    success_message_singular = _(
        message='%(count)d tag deleted successfully.'
    )
    title_plural = _(message='Delete the %(count)d selected tags')
    title_single = _(message='Delete tag: %(object)s')
    title_singular = _(message='Delete the %(count)d selected tag')
    view_icon = icon_tag_single_delete

    def get_extra_context(self):
        context = super().get_extra_context()
        context = {
            'message': _(message='Will be removed from all documents.')
        }

        return context


class TagEditView(SingleObjectEditView):
    form_class = TagForm
    model = Tag
    object_permission = permission_tag_edit
    pk_url_kwarg = 'tag_id'
    view_icon = icon_tag_edit

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _(message='Edit tag: %s') % self.object
        }

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}


class TagListView(SingleObjectListView):
    object_permission = permission_tag_view
    tag_model = Tag
    view_icon = icon_tag_list

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_menu_tags,
            'no_results_main_link': link_tag_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                message='Tags are color coded properties that can be attached or '
                'removed from documents.'
            ),
            'no_results_title': _(message='No tags available'),
            'title': _(message='Tags')
        }

    def get_source_queryset(self):
        queryset = ModelQueryFields.get(model=self.tag_model).get_queryset()
        return queryset.filter(
            pk__in=self.get_tag_queryset()
        )

    def get_tag_queryset(self):
        return Tag.objects.all()


class TagDocumentListView(ExternalObjectViewMixin, DocumentListView):
    external_object_class = Tag
    external_object_permission = permission_tag_view
    external_object_pk_url_kwarg = 'tag_id'
    view_icon = icon_tag_document_list

    def get_document_queryset(self):
        return Document.valid.filter(
            pk__in=self.get_tag().get_documents(
                permission=permission_document_view,
                user=self.request.user
            ).values('pk')
        )

    def get_extra_context(self):
        context = super().get_extra_context()
        context.update(
            {
                'object': self.get_tag(),
                'title': _(
                    message='Documents with the tag: %s'
                ) % self.get_tag()
            }
        )
        return context

    def get_tag(self):
        return self.external_object


class DocumentTagListView(ExternalObjectViewMixin, TagListView):
    external_object_permission = permission_tag_view
    external_object_pk_url_kwarg = 'document_id'
    external_object_queryset = Document.valid.all()
    tag_model = DocumentTag
    view_icon = icon_document_tag_list

    def get_extra_context(self):
        context = super().get_extra_context()
        context.update(
            {
                'hide_link': True,
                'no_results_main_link': link_document_tag_multiple_attach.resolve(
                    context=RequestContext(
                        dict_={'object': self.external_object},
                        request=self.request
                    )
                ),
                'no_results_title': _(
                    message='Document has no tags attached'
                ),
                'object': self.external_object,
                'title': _(
                    message='Tags for document: %s'
                ) % self.external_object
            }
        )
        return context

    def get_tag_queryset(self):
        return self.external_object.get_tags(
            permission=permission_tag_view, user=self.request.user
        )


class TagRemoveActionView(MultipleObjectFormActionView):
    form_class = TagMultipleSelectionForm
    object_permission = permission_tag_remove
    pk_url_kwarg = 'document_id'
    source_queryset = Document.valid.all()
    success_message_plural = _(
        message='Tags removed from %(count)d documents successfully.'
    )
    success_message_single = _(
        message='Tags removed from document "%(object)s" successfully.'
    )
    success_message_singular = _(
        message='Tags removed from %(count)d document successfully.'
    )
    title_plural = _(message='Remove tags from %(count)d documents.')
    title_single = _(message='Remove tags from document: %(object)s')
    title_singular = _(message='Remove tags from %(count)d document.')
    view_icon = icon_document_tag_multiple_remove

    def get_extra_context(self):
        context = {}

        if self.object_list.count() == 1:
            context.update(
                {
                    'object': self.object_list.first()
                }
            )

        return context

    def get_form_extra_kwargs(self):
        kwargs = {
            'help_text': _(message='Tags to be removed.'),
            'permission': permission_tag_remove,
            'queryset': Tag.objects.all(),
            'user': self.request.user
        }

        if self.object_list.count() == 1:
            kwargs.update(
                {
                    'queryset': self.object_list.first().tags.all()
                }
            )

        return kwargs

    def get_post_action_redirect(self):
        if self.object_list.count() == 1:
            return reverse(
                kwargs={
                    'document_id': self.object_list.first().pk
                }, viewname='tags:document_tag_list'
            )
        else:
            return super().get_post_action_redirect()

    def object_action(self, form, instance):
        for tag in form.cleaned_data['tags']:
            AccessControlList.objects.check_access(
                obj=tag, permission=permission_tag_remove,
                user=self.request.user
            )

            tag.remove_from(document=instance, user=self.request.user)
