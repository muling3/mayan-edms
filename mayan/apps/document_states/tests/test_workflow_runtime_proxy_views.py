from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..permissions import permission_workflow_template_view

from .mixins.workflow_runtime_proxy_mixins import (
    WorkflowRuntimeProxyStateViewTestMixin, WorkflowRuntimeProxyViewTestMixin
)
from .mixins.workflow_template_mixins import WorkflowTemplateTestMixin


class WorkflowRuntimeProxyViewTestCase(
    WorkflowRuntimeProxyViewTestMixin, WorkflowTemplateTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()
        self._create_test_document_stub()

    def test_workflow_runtime_proxy_document_list_view_no_permission(self):
        self._clear_events()

        response = self._request_test_workflow_runtime_proxy_document_list_view()
        self.assertNotContains(
            response=response, status_code=404,
            text=self._test_workflow_template.label
        )
        self.assertNotContains(
            response=response, status_code=404, text=self._test_document.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_runtime_proxy_document_list_view_with_workflow_access(self):
        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_runtime_proxy_document_list_view()
        self.assertContains(
            response=response, status_code=200,
            text=self._test_workflow_template.label
        )
        self.assertNotContains(
            response=response, status_code=200, text=self._test_document.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_runtime_proxy_document_list_view_with_document_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_workflow_runtime_proxy_document_list_view()
        self.assertNotContains(
            response=response, status_code=404,
            text=self._test_workflow_template.label
        )
        self.assertNotContains(
            response=response, status_code=404, text=self._test_document.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_runtime_proxy_document_list_view_with_full_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )
        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_runtime_proxy_document_list_view()
        self.assertContains(
            response=response, status_code=200,
            text=self._test_workflow_template.label
        )
        self.assertContains(
            response=response, status_code=200, text=self._test_document.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_workflow_runtime_proxy_document_list_view_with_full_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )
        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_workflow_runtime_proxy_document_list_view()
        self.assertContains(
            response=response, status_code=200,
            text=self._test_workflow_template.label
        )
        self.assertNotContains(
            response=response, status_code=200, text=self._test_document.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_runtime_proxy_list_view_no_permission(self):
        self._clear_events()

        response = self._request_test_workflow_runtime_proxy_list_view()
        self.assertNotContains(
            response=response, status_code=200,
            text=self._test_workflow_template.label
        )

    def test_workflow_runtime_proxy_list_view_with_access(self):
        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_runtime_proxy_list_view()
        self.assertContains(
            response=response, status_code=200,
            text=self._test_workflow_template.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class WorkflowRuntimeProxyStateViewTestCase(
    WorkflowRuntimeProxyStateViewTestMixin, WorkflowTemplateTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()
        self._create_test_document_stub()

    def test_workflow_runtime_proxy_state_document_list_view_no_permission(self):
        self._clear_events()

        response = self._request_test_workflow_runtime_proxy_state_document_list_view()
        self.assertNotContains(
            response=response, status_code=404,
            text=self._test_workflow_template_state_list[0].label
        )
        self.assertNotContains(
            response=response, status_code=404, text=self._test_document.label
        )
        self.assertNotContains(
            response=response, status_code=404, text=self._test_document.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_runtime_proxy_state_document_list_view_with_workflow_access(self):
        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_runtime_proxy_state_document_list_view()
        self.assertContains(
            response=response, status_code=200,
            text=self._test_workflow_template_state_list[0].label
        )
        self.assertNotContains(
            response=response, status_code=200, text=self._test_document.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_runtime_proxy_state_document_list_view_with_document_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_workflow_runtime_proxy_state_document_list_view()
        self.assertNotContains(
            response=response, status_code=404,
            text=self._test_workflow_template_state_list[0].label
        )
        self.assertNotContains(
            response=response, status_code=404, text=self._test_document.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_runtime_proxy_state_document_list_view_with_full_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )
        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_runtime_proxy_state_document_list_view()
        self.assertContains(
            response=response, status_code=200,
            text=self._test_workflow_template_state_list[0].label
        )
        self.assertContains(
            response=response, status_code=200, text=self._test_document.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_workflow_runtime_proxy_state_document_list_view_with_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )
        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_workflow_runtime_proxy_state_document_list_view()
        self.assertContains(
            response=response, status_code=200,
            text=self._test_workflow_template_state_list[0].label
        )
        self.assertNotContains(
            response=response, status_code=200, text=self._test_document.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_runtime_proxy_state_list_view_no_permission(self):
        self._clear_events()

        response = self._request_test_workflow_runtime_proxy_state_list_view()
        self.assertNotContains(
            response=response, status_code=404,
            text=self._test_workflow_template_state_list[0].label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_runtime_proxy_state_list_view_with_access(self):
        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_runtime_proxy_state_list_view()
        self.assertContains(
            response=response, status_code=200,
            text=self._test_workflow_template_state_list[0].label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
