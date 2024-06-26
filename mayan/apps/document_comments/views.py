from django.template import RequestContext
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from mayan.apps.documents.models.document_models import Document
from mayan.apps.views.generics import (
    SingleObjectCreateView, SingleObjectDeleteView, SingleObjectDetailView,
    SingleObjectEditView, SingleObjectListView
)
from mayan.apps.views.view_mixins import ExternalObjectViewMixin

from .forms import DocumentCommentDetailForm
from .icons import (
    icon_comment_add, icon_comment_delete, icon_comment_detail,
    icon_comment_edit, icon_comments_for_document
)
from .links import link_comment_add
from .models import Comment
from .permissions import (
    permission_document_comment_create, permission_document_comment_delete,
    permission_document_comment_edit, permission_document_comment_view
)


class DocumentCommentCreateView(
    ExternalObjectViewMixin, SingleObjectCreateView
):
    external_object_permission = permission_document_comment_create
    external_object_pk_url_kwarg = 'document_id'
    external_object_queryset = Document.valid.all()
    fields = ('text',)
    view_icon = icon_comment_add

    def get_extra_context(self):
        return {
            'object': self.external_object,
            'title': _(
                message='Add comment to document: %s'
            ) % self.external_object
        }

    def get_instance_extra_data(self):
        return {
            'document': self.external_object,
            'user': self.request.user
        }

    def get_post_action_redirect(self):
        return reverse(
            kwargs={
                'document_id': self.kwargs['document_id']
            }, viewname='comments:comments_for_document'
        )

    def get_queryset(self):
        return self.external_object.comments.all()


class DocumentCommentDeleteView(SingleObjectDeleteView):
    object_permission = permission_document_comment_delete
    pk_url_kwarg = 'comment_id'
    view_icon = icon_comment_delete

    def get_extra_context(self):
        return {
            'comment': self.object,
            'document': self.object.document,
            'navigation_object_list': ('document', 'comment'),
            'title': _(message='Delete comment: %s?') % self.object
        }

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}

    def get_post_action_redirect(self):
        return reverse(
            kwargs={'document_id': self.object.document_id},
            viewname='comments:comments_for_document'
        )

    def get_source_queryset(self):
        return Comment.objects.filter(
            document_id__in=Document.valid.values('id')
        )


class DocumentCommentDetailView(SingleObjectDetailView):
    form_class = DocumentCommentDetailForm
    pk_url_kwarg = 'comment_id'
    object_permission = permission_document_comment_view
    view_icon = icon_comment_detail

    def get_extra_context(self):
        return {
            'comment': self.object,
            'document': self.object.document,
            'navigation_object_list': ('document', 'comment'),
            'title': _(message='Details for comment: %s?') % self.object
        }

    def get_source_queryset(self):
        return Comment.objects.filter(
            document_id__in=Document.valid.values('id')
        )


class DocumentCommentEditView(SingleObjectEditView):
    fields = ('text',)
    pk_url_kwarg = 'comment_id'
    object_permission = permission_document_comment_edit
    view_icon = icon_comment_edit

    def get_extra_context(self):
        return {
            'comment': self.object,
            'document': self.object.document,
            'navigation_object_list': ('document', 'comment'),
            'title': _(message='Edit comment: %s?') % self.object
        }

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}

    def get_post_action_redirect(self):
        return reverse(
            kwargs={'document_id': self.object.document_id},
            viewname='comments:comments_for_document'
        )

    def get_source_queryset(self):
        return Comment.objects.filter(
            document_id__in=Document.valid.values('id')
        )


class DocumentCommentListView(ExternalObjectViewMixin, SingleObjectListView):
    external_object_permission = permission_document_comment_view
    external_object_pk_url_kwarg = 'document_id'
    external_object_queryset = Document.valid.all()
    view_icon = icon_comments_for_document

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_comments_for_document,
            'no_results_external_link': link_comment_add.resolve(
                RequestContext(
                    dict_={'object': self.external_object},
                    request=self.request
                )
            ),
            'no_results_text': _(
                message='Document comments are timestamped text entries from '
                'users. They are great for collaboration.'
            ),
            'no_results_title': _(message='There are no comments'),
            'object': self.external_object,
            'title': _(
                message='Comments for document: %s'
            ) % self.external_object
        }

    def get_source_queryset(self):
        return self.external_object.comments.all()
