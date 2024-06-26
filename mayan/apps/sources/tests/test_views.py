from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import event_source_created, event_source_edited
from ..models import Source
from ..permissions import (
    permission_document_file_sources_metadata_view, permission_sources_create,
    permission_sources_delete, permission_sources_edit,
    permission_sources_view
)

from .literals import (
    TEST_SOURCE_ACTION_CONFIRM_FALSE_NAME,
    TEST_SOURCE_ACTION_CONFIRM_TRUE_NAME, TEST_SOURCE_LABEL,
    TEST_SOURCE_METADATA_KEY, TEST_SOURCE_METADATA_VALUE
)
from .mixins.source_view_mixins import (
    DocumentFileSourceMetadataViewTestMixin, SourceActionViewTestMixin,
    SourceViewTestMixin
)


class DocumentSourceMetadataViewTestCase(
    DocumentFileSourceMetadataViewTestMixin, GenericViewTestCase
):
    def test_document_file_source_metadata_list_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_file_source_metadata_list_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_source_metadata_list_view_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_file_sources_metadata_view
        )

        self._clear_events()

        response = self._request_test_document_file_source_metadata_list_view()
        self.assertContains(
            response=response, status_code=200,
            text=TEST_SOURCE_METADATA_KEY
        )
        self.assertContains(
            response=response, status_code=200,
            text=TEST_SOURCE_METADATA_VALUE
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class SourceActionViewTestCase(
    SourceActionViewTestMixin, GenericViewTestCase
):
    def test_source_action_get_view_no_permission(self):
        self._clear_events()

        response = self._request_test_source_action_get_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_action_get_view_with_access(self):
        action = self._test_source.get_action(
            name=TEST_SOURCE_ACTION_CONFIRM_FALSE_NAME
        )

        self.grant_access(
            obj=self._test_source, permission=action.permission
        )

        self._clear_events()

        response = self._request_test_source_action_get_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_action_post_view_no_permission(self):
        self._clear_events()

        response = self._request_test_source_action_post_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_action_post_view_with_access(self):
        action = self._test_source.get_action(
            name=TEST_SOURCE_ACTION_CONFIRM_TRUE_NAME
        )

        self.grant_access(
            obj=self._test_source, permission=action.permission
        )

        self._clear_events()

        response = self._request_test_source_action_post_view()
        self.assertEqual(response.status_code, 302)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class SourceViewTestCase(SourceViewTestMixin, GenericViewTestCase):
    _test_source_create_auto = False

    def test_source_create_get_view_no_permission(self):
        source_count = Source.objects.count()

        self._clear_events()

        response = self._request_test_source_create_get_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Source.objects.count(), source_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_create_get_view_with_permission(self):
        self.grant_permission(permission=permission_sources_create)

        source_count = Source.objects.count()

        self._clear_events()

        response = self._request_test_source_create_get_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Source.objects.count(), source_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_create_post_view_no_permission(self):
        source_count = Source.objects.count()

        self._clear_events()

        response = self._request_test_source_create_post_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Source.objects.count(), source_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_create_post_view_with_permission(self):
        self.grant_permission(permission=permission_sources_create)

        source_count = Source.objects.count()

        self._clear_events()

        response = self._request_test_source_create_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self._test_source.label, '{}_0'.format(TEST_SOURCE_LABEL)
        )
        self.assertEqual(Source.objects.count(), source_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_source)
        self.assertEqual(events[0].verb, event_source_created.id)

    def test_source_delete_view_no_permission(self):
        self._test_source_create()

        source_count = Source.objects.count()

        self._clear_events()

        response = self._request_test_source_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Source.objects.count(), source_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_delete_view_with_access(self):
        self._test_source_create()

        self.grant_access(
            obj=self._test_source, permission=permission_sources_delete
        )

        source_count = Source.objects.count()

        self._clear_events()

        response = self._request_test_source_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Source.objects.count(), source_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_edit_view_no_permission(self):
        self._test_source_create()
        test_instance_values = self._model_instance_to_dictionary(
            instance=self._test_source
        )

        self._clear_events()

        response = self._request_test_source_edit_view()
        self.assertEqual(response.status_code, 404)

        self._test_source.refresh_from_db()
        self.assertEqual(
            self._model_instance_to_dictionary(
                instance=self._test_source
            ), test_instance_values
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_edit_view_with_access(self):
        self._test_source_create()
        test_instance_values = self._model_instance_to_dictionary(
            instance=self._test_source
        )
        self.grant_access(
            obj=self._test_source, permission=permission_sources_edit
        )

        self._clear_events()

        response = self._request_test_source_edit_view()
        self.assertEqual(response.status_code, 302)

        self._test_source.refresh_from_db()
        self.assertNotEqual(
            self._model_instance_to_dictionary(
                instance=self._test_source
            ), test_instance_values
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_source)
        self.assertEqual(events[0].verb, event_source_edited.id)

    def test_source_list_view_no_permission(self):
        self._test_source_create()

        self._clear_events()

        response = self._request_test_source_list_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_list_view_with_access(self):
        self._test_source_create()

        self.grant_access(
            obj=self._test_source, permission=permission_sources_view
        )

        self._clear_events()

        response = self._request_test_source_list_view()
        self.assertContains(
            response=response, text=self._test_source.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
