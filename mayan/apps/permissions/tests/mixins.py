from django.db.models import Q

from ..classes import Permission, PermissionNamespace
from ..models import Role

from .literals import (
    TEST_CASE_ROLE_LABEL, TEST_PERMISSION_LABEL, TEST_PERMISSION_NAME,
    TEST_PERMISSION_NAMESPACE_LABEL, TEST_PERMISSION_NAMESPACE_NAME,
    TEST_ROLE_LABEL, TEST_ROLE_LABEL_EDITED
)


class PermissionAPIViewTestMixin:
    def _request_permissions_list_api_view(self):
        return self.get(viewname='rest_api:permission-list')


class PermissionTestMixin:
    def setUp(self):
        super().setUp()
        self._test_permission_list = []

    def _create_test_permission(self):
        self._test_permission_namespace = PermissionNamespace(
            label=TEST_PERMISSION_NAMESPACE_LABEL,
            name=TEST_PERMISSION_NAMESPACE_NAME
        )

        test_permission_count = len(self._test_permission_list)
        self._test_permission = self._test_permission_namespace.add_permission(
            label='{}_{}'.format(
                TEST_PERMISSION_LABEL, test_permission_count
            ), name='{}_{}'.format(
                TEST_PERMISSION_NAME, test_permission_count
            )
        )
        self._test_permission_list.append(self._test_permission)


class PermissionTestCaseMixin:
    def setUp(self):
        super().setUp()
        Permission.invalidate_cache()


class RoleTestMixin:
    def setUp(self):
        super().setUp()
        self._test_role_list = []

    def _create_test_role(self, add_groups=None):
        total_test_role_count = len(self._test_role_list)
        label = '{}_{}'.format(TEST_ROLE_LABEL, total_test_role_count)

        self._test_role = Role.objects.create(label=label)

        self._test_role_list.append(self._test_role)

        for group in add_groups or []:
            self._test_role.groups.add(group)


class GroupRoleAddRemoveViewTestMixin(RoleTestMixin):
    def _request_test_group_role_add_remove_get_view(self):
        return self.get(
            viewname='permissions:group_role_list', kwargs={
                'group_id': self._test_group.pk
            }
        )

    def _request_test_group_role_add_view(self):
        return self.post(
            viewname='permissions:group_role_list', kwargs={
                'group_id': self._test_group.pk,
            }, data={
                'available-selection': self._test_role.pk,
                'available-submit': 'true'
            }
        )

    def _request_test_group_role_remove_view(self):
        return self.post(
            viewname='permissions:group_role_list', kwargs={
                'group_id': self._test_group.pk,
            }, data={
                'added-selection': self._test_role.pk,
                'added-submit': 'true'
            }
        )


class RoleAPIViewTestMixin(RoleTestMixin):
    def _request_test_role_create_api_view(self, extra_data=None):
        pk_list = list(
            Role.objects.values_list('pk', flat=True)
        )

        data = {'label': TEST_ROLE_LABEL}

        if extra_data:
            data.update(extra_data)

        response = self.post(
            viewname='rest_api:role-list', data=data
        )

        try:
            self._test_role = Role.objects.get(
                ~Q(pk__in=pk_list)
            )
        except Role.DoesNotExist:
            self._test_role = None

        return response

    def _request_test_role_delete_api_view(self):
        return self.delete(
            viewname='rest_api:role-detail', kwargs={
                'role_id': self._test_role.pk
            }
        )

    def _request_test_role_edit_api_view(
        self, extra_data=None, request_type='patch'
    ):
        data = {'label': TEST_ROLE_LABEL_EDITED}

        if extra_data:
            data.update(extra_data)

        return getattr(self, request_type)(
            viewname='rest_api:role-detail', kwargs={
                'role_id': self._test_role.pk
            }, data=data
        )

    def _request_test_role_edit_api_patch_view_extra_data(self):
        extra_data = {
            'groups_pk_list': '{}'.format(self._test_group.pk),
            'permissions_pk_list': '{}'.format(self._test_permission.pk)
        }
        return self._request_test_role_edit_api_view(
            extra_data=extra_data, request_type='patch'
        )

    def _request_test_role_edit_api_put_view_extra_data(self):
        extra_data = {
            'groups_pk_list': '{}'.format(self._test_group.pk),
            'permissions_pk_list': '{}'.format(self._test_permission.pk)
        }
        return self._request_test_role_edit_api_view(
            extra_data=extra_data, request_type='put'
        )

    def _request_test_role_list_api_view(self):
        return self.get(viewname='rest_api:role-list')


class RoleGroupAPIViewTestMixin(RoleTestMixin):
    def _request_test_role_group_add_api_view(self):
        return self.post(
            viewname='rest_api:role-group-add', kwargs={
                'role_id': self._test_role.pk
            }, data={'group': self._test_group.pk}
        )

    def _request_test_role_group_list_api_view(self):
        return self.get(
            viewname='rest_api:role-group-list', kwargs={
                'role_id': self._test_role.pk
            }
        )

    def _request_test_role_group_remove_api_view(self):
        return self.post(
            viewname='rest_api:role-group-remove', kwargs={
                'role_id': self._test_role.pk
            }, data={'group': self._test_group.pk}
        )


class RolePermissionAPIViewTestMixin(RoleTestMixin):
    def _request_test_role_permission_add_api_view(self):
        return self.post(
            viewname='rest_api:role-permission-add', kwargs={
                'role_id': self._test_role.pk
            }, data={'permission': self._test_permission.pk}
        )

    def _request_test_role_permission_list_api_view(self):
        return self.get(
            viewname='rest_api:role-permission-list', kwargs={
                'role_id': self._test_role.pk
            }
        )

    def _request_test_role_permission_remove_api_view(self):
        return self.post(
            viewname='rest_api:role-permission-remove', kwargs={
                'role_id': self._test_role.pk
            }, data={'permission': self._test_permission.pk}
        )


class RoleTestCaseMixin:
    def setUp(self):
        super().setUp()
        if hasattr(self, '_test_case_group'):
            self.create_role()

    def create_role(self):
        self._test_case_role = Role.objects.create(
            label=TEST_CASE_ROLE_LABEL
        )

    def grant_permission(self, permission):
        self._test_case_role.grant(permission=permission)

    def revoke_permission(self, permission):
        self._test_case_role.revoke(permission=permission)


class RoleGroupAddRemoveViewTestMixin(RoleTestMixin):
    def _request_test_role_group_add_remove_get_view(self):
        return self.get(
            viewname='permissions:role_group_list', kwargs={
                'role_id': self._test_role.pk
            }
        )

    def _request_test_role_group_add_view(self):
        return self.post(
            viewname='permissions:role_group_list', kwargs={
                'role_id': self._test_role.pk
            }, data={
                'available-submit': 'true',
                'available-selection': self._test_group.pk
            }
        )

    def _request_test_role_group_remove_view(self):
        return self.post(
            viewname='permissions:role_group_list', kwargs={
                'role_id': self._test_role.pk
            }, data={
                'added-submit': 'true',
                'added-selection': self._test_group.pk
            }
        )


class RolePermissionAddRemoveViewTestMixin(RoleTestMixin):
    def _request_test_role_permission_add_remove_get_view(self):
        return self.get(
            viewname='permissions:role_permission_list', kwargs={
                'role_id': self._test_role.pk
            }
        )

    def _request_test_role_permission_add_view(self):
        return self.post(
            viewname='permissions:role_permission_list', kwargs={
                'role_id': self._test_role.pk
            }, data={
                'available-selection': self._test_permission.stored_permission.pk,
                'available-submit': 'true'
            }
        )

    def _request_test_role_permission_remove_view(self):
        return self.post(
            viewname='permissions:role_permission_list', kwargs={
                'role_id': self._test_role.pk
            }, data={
                'added-selection': self._test_permission.stored_permission.pk,
                'added-submit': 'true'
            }
        )


class RoleViewTestMixin(RoleTestMixin):
    def _request_test_role_create_view(self):
        pk_list = list(
            Role.objects.values_list('pk', flat=True)
        )

        response = self.post(
            viewname='permissions:role_create', data={
                'label': TEST_ROLE_LABEL
            }
        )

        try:
            self._test_role = Role.objects.get(
                ~Q(pk__in=pk_list)
            )
        except Role.DoesNotExist:
            self._test_role = None

        return response

    def _request_test_role_single_delete_view(self):
        return self.post(
            viewname='permissions:role_single_delete', kwargs={
                'role_id': self._test_role.pk
            }
        )

    def _request_test_role_multiple_delete_view(self):
        return self.post(
            viewname='permissions:role_multiple_delete', data={
                'id_list': self._test_role.pk
            }
        )

    def _request_test_role_edit_view(self):
        return self.post(
            viewname='permissions:role_edit', kwargs={
                'role_id': self._test_role.pk
            }, data={
                'label': TEST_ROLE_LABEL_EDITED
            }
        )

    def _request_test_role_list_view(self):
        return self.get(viewname='permissions:role_list')
