from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import (
    event_tag_attached, event_tag_created, event_tag_edited, event_tag_removed
)
from ..links import link_tag_edit
from ..models import Tag
from ..permissions import (
    permission_tag_attach, permission_tag_create, permission_tag_delete,
    permission_tag_edit, permission_tag_remove, permission_tag_view
)

from .mixins import DocumentTagViewTestMixin, TagViewTestMixin


class DocumentTagViewTestCase(
    DocumentTagViewTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()

    def test_document_tags_list_no_permission(self):
        self._create_test_tag(add_test_document=True)

        self._clear_events()

        response = self._request_test_document_tag_list_view()
        self.assertNotContains(
            response=response, text=str(self._test_tag), status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_tags_list_with_document_access(self):
        self._create_test_tag(add_test_document=True)

        self.grant_access(
            obj=self._test_document, permission=permission_tag_view
        )

        self._clear_events()

        response = self._request_test_document_tag_list_view()
        self.assertNotContains(
            response=response, text=str(self._test_tag), status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_tags_list_with_tag_access(self):
        self._create_test_tag(add_test_document=True)

        self.grant_access(obj=self._test_tag, permission=permission_tag_view)

        self._clear_events()

        response = self._request_test_document_tag_list_view()
        self.assertNotContains(
            response=response, text=str(self._test_tag), status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_tags_list_with_full_access(self):
        self._create_test_tag(add_test_document=True)

        self.grant_access(
            obj=self._test_document, permission=permission_tag_view
        )
        self.grant_access(
            obj=self._test_tag, permission=permission_tag_view
        )

        self._clear_events()

        response = self._request_test_document_tag_list_view()
        self.assertContains(
            response=response, text=str(self._test_tag),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_tags_list_with_full_access(self):
        self._create_test_tag(add_test_document=True)

        self.grant_access(
            obj=self._test_document, permission=permission_tag_view
        )
        self.grant_access(
            obj=self._test_tag, permission=permission_tag_view
        )

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_document_tag_list_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_tags_list_tag_edit_link_with_full_access(self):
        # Ensure that `DocumentTag` instances and links are
        # resolved in this view and not base Tag instances.
        self._create_test_tag(add_test_document=True)

        self.grant_access(
            obj=self._test_document, permission=permission_tag_view
        )
        self.grant_access(
            obj=self._test_tag, permission=permission_tag_edit
        )
        self.grant_access(
            obj=self._test_tag, permission=permission_tag_view
        )

        self._clear_events()

        response = self._request_test_document_tag_list_view()

        # Get the first context item that correspond to an an item in the
        # response nexted context list.
        for context in response.context:
            if 'object' in context:
                break

        context['object'] = self._test_tag

        result = link_tag_edit.resolve(context=context)

        self.assertNotContains(
            response=response, text=result.url,
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_tag_attach_view_no_permission(self):
        self._create_test_tag()

        self._clear_events()

        response = self._request_test_document_tag_attach_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self._test_tag not in self._test_document.tags.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_tag_attach_view_with_tag_access(self):
        self._create_test_tag()

        self.grant_access(
            obj=self._test_tag, permission=permission_tag_attach
        )

        self._clear_events()

        response = self._request_test_document_tag_attach_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self._test_tag not in self._test_document.tags.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_tag_attach_view_with_document_access(self):
        self._create_test_tag()

        self.grant_access(
            obj=self._test_document, permission=permission_tag_attach
        )

        self._clear_events()

        response = self._request_test_document_tag_attach_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            self._test_tag not in self._test_document.tags.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_tag_attach_view_with_full_access(self):
        self._create_test_tag()

        self.grant_access(
            obj=self._test_document, permission=permission_tag_attach
        )
        self.grant_access(
            obj=self._test_tag, permission=permission_tag_attach
        )

        self._clear_events()

        response = self._request_test_document_tag_attach_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self._test_tag in self._test_document.tags.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_tag)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_document)
        self.assertEqual(events[0].verb, event_tag_attached.id)

    def test_trashed_document_tag_attach_view_with_full_access(self):
        self._create_test_tag()

        self.grant_access(
            obj=self._test_document, permission=permission_tag_attach
        )
        self.grant_access(
            obj=self._test_tag, permission=permission_tag_attach
        )

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_document_tag_attach_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self._test_tag not in self._test_document.tags.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_multiple_tag_attach_view_no_permission(self):
        self._create_test_tag()

        self._clear_events()

        response = self._request_test_document_multiple_tag_multiple_attach_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self._test_tag not in self._test_document.tags.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_multiple_tag_attach_view_with_tag_access(self):
        self._create_test_tag()

        self.grant_access(
            obj=self._test_tag, permission=permission_tag_attach
        )

        self._clear_events()

        response = self._request_test_document_multiple_tag_multiple_attach_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self._test_tag not in self._test_document.tags.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_multiple_tag_attach_view_with_document_access(self):
        self._create_test_tag()

        self.grant_access(
            obj=self._test_document, permission=permission_tag_attach
        )

        self._clear_events()

        response = self._request_test_document_multiple_tag_multiple_attach_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            self._test_tag not in self._test_document.tags.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_multiple_tag_attach_view_with_full_access(self):
        self._create_test_tag()

        self.grant_access(
            obj=self._test_document, permission=permission_tag_attach
        )
        self.grant_access(
            obj=self._test_tag, permission=permission_tag_attach
        )

        self._clear_events()

        response = self._request_test_document_multiple_tag_multiple_attach_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self._test_tag in self._test_document.tags.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_tag)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_document)
        self.assertEqual(events[0].verb, event_tag_attached.id)

    def test_trashed_document_multiple_tag_attach_view_with_full_access(self):
        self._create_test_tag()

        self.grant_access(
            obj=self._test_document, permission=permission_tag_attach
        )
        self.grant_access(
            obj=self._test_tag, permission=permission_tag_attach
        )

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_document_multiple_tag_multiple_attach_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self._test_tag not in self._test_document.tags.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_tag_multiple_remove_view_no_permission(self):
        self._create_test_tag()
        self._test_document.tags.add(self._test_tag)

        self._clear_events()

        response = self._request_test_document_tag_multiple_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self._test_tag in self._test_document.tags.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_tag_multiple_remove_view_with_tag_access(self):
        self._create_test_tag()
        self._test_document.tags.add(self._test_tag)

        self.grant_access(
            obj=self._test_tag, permission=permission_tag_remove
        )

        self._clear_events()

        response = self._request_test_document_tag_multiple_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self._test_tag in self._test_document.tags.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_tag_multiple_remove_view_with_document_access(self):
        self._create_test_tag()
        self._test_document.tags.add(self._test_tag)

        self.grant_access(
            obj=self._test_document, permission=permission_tag_remove
        )

        self._clear_events()

        response = self._request_test_document_tag_multiple_remove_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            self._test_tag in self._test_document.tags.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_tag_multiple_remove_view_with_full_access(self):
        self._create_test_tag()
        self._test_document.tags.add(self._test_tag)

        self.grant_access(
            obj=self._test_document, permission=permission_tag_remove
        )
        self.grant_access(
            obj=self._test_tag, permission=permission_tag_remove
        )

        self._clear_events()

        response = self._request_test_document_tag_multiple_remove_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self._test_tag not in self._test_document.tags.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_tag)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_document)
        self.assertEqual(events[0].verb, event_tag_removed.id)

    def test_trashed_document_tag_multiple_remove_view_with_full_access(self):
        self._create_test_tag()
        self._test_document.tags.add(self._test_tag)

        self.grant_access(
            obj=self._test_document, permission=permission_tag_remove
        )
        self.grant_access(
            obj=self._test_tag, permission=permission_tag_remove
        )

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_document_tag_multiple_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self._test_tag in self._test_document.tags.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_multiple_tag_multiple_remove_view_no_permission(self):
        self._create_test_tag()
        self._test_document.tags.add(self._test_tag)

        self._clear_events()

        response = self._request_test_document_multiple_tag_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self._test_tag in self._test_document.tags.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_multiple_tag_remove_view_with_tag_access(self):
        self._create_test_tag()
        self._test_document.tags.add(self._test_tag)

        self.grant_access(
            obj=self._test_tag, permission=permission_tag_remove
        )

        self._clear_events()

        response = self._request_test_document_multiple_tag_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self._test_tag in self._test_document.tags.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_multiple_tag_remove_view_with_document_access(self):
        self._create_test_tag()
        self._test_document.tags.add(self._test_tag)

        self.grant_access(
            obj=self._test_document, permission=permission_tag_remove
        )

        self._clear_events()

        response = self._request_test_document_multiple_tag_remove_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            self._test_tag in self._test_document.tags.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_multiple_tag_remove_view_with_full_access(self):
        self._create_test_tag()
        self._test_document.tags.add(self._test_tag)

        self.grant_access(
            obj=self._test_document, permission=permission_tag_remove
        )
        self.grant_access(
            obj=self._test_tag, permission=permission_tag_remove
        )

        self._clear_events()

        response = self._request_test_document_multiple_tag_remove_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self._test_tag not in self._test_document.tags.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_tag)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_document)
        self.assertEqual(events[0].verb, event_tag_removed.id)

    def test_trashed_document_multiple_tag_remove_view_with_full_access(self):
        self._create_test_tag()
        self._test_document.tags.add(self._test_tag)

        self.grant_access(
            obj=self._test_document, permission=permission_tag_remove
        )
        self.grant_access(
            obj=self._test_tag, permission=permission_tag_remove
        )

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_document_multiple_tag_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self._test_tag in self._test_document.tags.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_tag_document_list_with_no_permission(self):
        self._create_test_tag(add_test_document=True)

        self._clear_events()

        response = self._request_test_tag_document_list_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_tag_document_list_with_tag_access(self):
        self._create_test_tag(add_test_document=True)

        self.grant_access(obj=self._test_tag, permission=permission_tag_view)

        self._clear_events()

        response = self._request_test_tag_document_list_view()
        self.assertContains(
            response=response, text=str(self._test_tag),
            status_code=200
        )
        self.assertNotContains(
            response=response, text=str(self._test_document),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_tag_document_list_with_document_access(self):
        self._create_test_tag(add_test_document=True)

        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_tag_document_list_view()
        self.assertNotContains(
            response=response, text=str(self._test_tag),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=str(self._test_document),
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_tag_document_list_with_full_access(self):
        self._create_test_tag(add_test_document=True)

        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )
        self.grant_access(obj=self._test_tag, permission=permission_tag_view)

        self._clear_events()

        response = self._request_test_tag_document_list_view()
        self.assertContains(
            response=response, text=str(self._test_tag),
            status_code=200
        )
        self.assertContains(
            response=response, text=str(self._test_document),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_tag_trashed_document_list_with_full_access(self):
        self._create_test_tag(add_test_document=True)

        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )
        self.grant_access(obj=self._test_tag, permission=permission_tag_view)

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_tag_document_list_view()
        self.assertContains(
            response=response, text=str(self._test_tag),
            status_code=200
        )
        self.assertNotContains(
            response=response, text=str(self._test_document),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class TagViewTestCase(TagViewTestMixin, GenericViewTestCase):
    def test_tag_create_view_no_permission(self):
        tag_count = Tag.objects.count()

        self._clear_events()

        response = self._request_test_tag_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Tag.objects.count(), tag_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_tag_create_view_with_permissions(self):
        self.grant_permission(permission=permission_tag_create)

        tag_count = Tag.objects.count()

        self._clear_events()

        response = self._request_test_tag_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Tag.objects.count(), tag_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_tag)
        self.assertEqual(events[0].verb, event_tag_created.id)

    def test_tag_delete_view_no_permission(self):
        self._create_test_tag()

        tag_count = Tag.objects.count()

        self._clear_events()

        response = self._request_test_tag_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Tag.objects.count(), tag_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_tag_delete_view_with_access(self):
        self._create_test_tag()

        self.grant_access(
            obj=self._test_tag, permission=permission_tag_delete
        )

        tag_count = Tag.objects.count()

        self._clear_events()

        response = self._request_test_tag_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Tag.objects.count(), tag_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_tag_multiple_delete_view_no_permission(self):
        self._create_test_tag()

        tag_count = Tag.objects.count()

        self._clear_events()

        response = self._request_test_tag_multiple_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Tag.objects.count(), tag_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_tag_multiple_delete_view_with_access(self):
        self._create_test_tag()

        self.grant_access(
            obj=self._test_tag, permission=permission_tag_delete
        )

        tag_count = Tag.objects.count()

        self._clear_events()

        response = self._request_test_tag_multiple_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Tag.objects.count(), tag_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_tag_edit_view_no_permission(self):
        self._create_test_tag()

        tag_label = self._test_tag.label

        self._clear_events()

        response = self._request_test_tag_edit_view()
        self.assertEqual(response.status_code, 404)

        self._test_tag.refresh_from_db()
        self.assertEqual(self._test_tag.label, tag_label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_tag_edit_view_with_access(self):
        self._create_test_tag()

        self.grant_access(obj=self._test_tag, permission=permission_tag_edit)

        tag_label = self._test_tag.label

        self._clear_events()

        response = self._request_test_tag_edit_view()
        self.assertEqual(response.status_code, 302)

        self._test_tag.refresh_from_db()
        self.assertNotEqual(self._test_tag.label, tag_label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_tag)
        self.assertEqual(events[0].verb, event_tag_edited.id)

    def test_tag_list_view_with_no_permission(self):
        self._create_test_tag()

        self._clear_events()

        response = self._request_test_tag_list_view()
        self.assertNotContains(
            response=response, text=self._test_tag.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_tag_list_view_with_access(self):
        self._create_test_tag()

        self.grant_access(obj=self._test_tag, permission=permission_tag_view)

        self._clear_events()

        response = self._request_test_tag_list_view()
        self.assertContains(
            response=response, text=self._test_tag.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
