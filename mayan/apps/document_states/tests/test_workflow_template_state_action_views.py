from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import event_workflow_template_edited
from ..permissions import permission_workflow_template_edit

from .literals import TEST_WORKFLOW_TEMPLATE_STATE_ACTION_DOTTED_PATH
from .mixins.workflow_template_state_action_mixins import (
    WorkflowTemplateStateActionViewTestMixin
)


class WorkflowStateActionViewTestCase(
    WorkflowTemplateStateActionViewTestMixin, GenericViewTestCase
):
    def test_workflow_state_action_create_get_view_no_permission(self):
        action_count = self._test_workflow_template_state.actions.count()

        self._clear_events()

        response = self._request_test_workflow_template_state_action_create_get_view(
            backend_path=TEST_WORKFLOW_TEMPLATE_STATE_ACTION_DOTTED_PATH
        )
        self.assertEqual(response.status_code, 404)

        self._test_workflow_template_state.refresh_from_db()
        self.assertEqual(
            self._test_workflow_template_state.actions.count(), action_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_state_action_create_get_view_with_access(self):
        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )
        action_count = self._test_workflow_template_state.actions.count()

        self._clear_events()

        response = self._request_test_workflow_template_state_action_create_get_view(
            backend_path=TEST_WORKFLOW_TEMPLATE_STATE_ACTION_DOTTED_PATH
        )
        self.assertEqual(response.status_code, 200)

        self._test_workflow_template_state.refresh_from_db()
        self.assertEqual(
            self._test_workflow_template_state.actions.count(), action_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_state_action_create_post_view_no_permission(self):
        action_count = self._test_workflow_template_state.actions.count()

        self._clear_events()

        response = self._request_test_workflow_template_state_action_create_post_view(
            backend_path=TEST_WORKFLOW_TEMPLATE_STATE_ACTION_DOTTED_PATH
        )
        self.assertEqual(response.status_code, 404)

        self._test_workflow_template_state.refresh_from_db()
        self.assertEqual(
            self._test_workflow_template_state.actions.count(), action_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_state_action_create_post_view_with_access(self):
        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )
        action_count = self._test_workflow_template_state.actions.count()

        self._clear_events()

        response = self._request_test_workflow_template_state_action_create_post_view(
            backend_path=TEST_WORKFLOW_TEMPLATE_STATE_ACTION_DOTTED_PATH
        )
        self.assertEqual(response.status_code, 302)

        self._test_workflow_template_state.refresh_from_db()
        self.assertEqual(
            self._test_workflow_template_state.actions.count(),
            action_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(
            events[0].action_object,
            self._test_workflow_template_state_action
        )
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_state_action_delete_view_no_permission(self):
        self._create_test_workflow_template_state_action()
        action_count = self._test_workflow_template_state.actions.count()

        self._clear_events()

        response = self._request_test_workflow_template_state_action_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self._test_workflow_template_state.actions.count(), action_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_state_action_delete_view_with_access(self):
        self._create_test_workflow_template_state_action()
        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )
        action_count = self._test_workflow_template_state.actions.count()

        self._clear_events()

        response = self._request_test_workflow_template_state_action_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self._test_workflow_template_state.actions.count(),
            action_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_state_action_edit_view_no_permission(self):
        self._create_test_workflow_template_state_action()
        action_label = self._test_workflow_template_state_action.label

        self._clear_events()

        response = self._request_test_workflow_template_state_action_edit_post_view()
        self.assertEqual(response.status_code, 404)

        self._test_workflow_template_state_action.refresh_from_db()
        self.assertEqual(
            self._test_workflow_template_state_action.label, action_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_state_action_edit_view_with_access(self):
        self._create_test_workflow_template_state_action()
        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )
        action_label = self._test_workflow_template_state_action.label

        self._clear_events()

        response = self._request_test_workflow_template_state_action_edit_post_view()
        self.assertEqual(response.status_code, 302)

        self._test_workflow_template_state_action.refresh_from_db()
        self.assertNotEqual(
            self._test_workflow_template_state_action.label, action_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(
            events[0].action_object,
            self._test_workflow_template_state_action
        )
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_state_action_list_view_no_permission(self):
        self._create_test_workflow_template_state_action()

        self._clear_events()

        response = self._request_test_workflow_template_state_action_list_view()
        self.assertNotContains(
            response=response, status_code=404,
            text=self._test_workflow_template_state_action.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_state_action_list_view_with_access(self):
        self._create_test_workflow_template_state_action()
        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_state_action_list_view()
        self.assertContains(
            response=response, status_code=200,
            text=self._test_workflow_template_state_action.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_state_action_selection_view_no_permission(self):
        action_count = self._test_workflow_template_state.actions.count()

        self._clear_events()

        response = self._request_test_workflow_template_state_action_selection_view()
        self.assertEqual(response.status_code, 404)

        self._test_workflow_template_state.refresh_from_db()
        self.assertEqual(
            self._test_workflow_template_state.actions.count(), action_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_state_action_selection_view_with_access(self):
        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )
        action_count = self._test_workflow_template_state.actions.count()

        self._clear_events()

        response = self._request_test_workflow_template_state_action_selection_view()
        self.assertEqual(response.status_code, 302)

        self._test_workflow_template_state.refresh_from_db()
        self.assertEqual(
            self._test_workflow_template_state.actions.count(), action_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
