from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from ..links import link_group_setup, link_user_setup

from .literals import (
    TEST_CASE_GROUP_NAME, TEST_CASE_SUPER_USER_EMAIL,
    TEST_CASE_SUPER_USER_PASSWORD, TEST_CASE_SUPER_USER_USERNAME,
    TEST_CASE_USER_EMAIL, TEST_CASE_USER_FIRST_NAME, TEST_CASE_USER_LAST_NAME,
    TEST_CASE_USER_PASSWORD, TEST_CASE_USER_USERNAME, TEST_GROUP_NAME,
    TEST_GROUP_NAME_EDITED, TEST_USER_EMAIL, TEST_USER_PASSWORD,
    TEST_USER_PASSWORD_EDITED, TEST_USER_USERNAME, TEST_USER_USERNAME_EDITED
)


class CurrentUserViewTestMixin:
    def _request_current_user_details_view(self, user=None):
        user = user or self._test_case_user

        return self.get(
            viewname='user_management:user_details', kwargs={
                'user_id': user.pk
            }
        )

    def _request_current_user_edit_view(self, user=None):
        user = user or self._test_case_user

        return self.get(
            viewname='user_management:user_edit', kwargs={
                'user_id': user.pk
            }
        )

    def _request_current_user_post_view(self, user=None):
        user = user or self._test_case_user

        return self.post(
            viewname='user_management:user_edit', kwargs={
                'user_id': user.pk
            }, data={
                'username': 'new_username', 'first_name': 'first name edited'
            }
        )


class GroupAPIViewTestMixin:
    def _request_test_group_create_api_view(self):
        result = self.post(
            viewname='rest_api:group-list', data={
                'name': TEST_GROUP_NAME
            }
        )
        if 'id' in result.json():
            self._test_group = Group.objects.get(
                pk=result.json()['id']
            )

        return result

    def _request_test_group_delete_api_view(self):
        return self.delete(
            viewname='rest_api:group-detail', kwargs={
                'group_id': self._test_group.pk
            }
        )

    def _request_test_group_detail_api_view(self):
        return self.get(
            viewname='rest_api:group-detail', kwargs={
                'group_id': self._test_group.pk
            }
        )

    def _request_test_group_edit_patch_api_view(self):
        return self.patch(
            viewname='rest_api:group-detail', kwargs={
                'group_id': self._test_group.pk
            }, data={
                'name': TEST_GROUP_NAME_EDITED
            }
        )

    def _request_test_group_edit_put_api_view(self):
        return self.put(
            viewname='rest_api:group-detail', kwargs={
                'group_id': self._test_group.pk
            }, data={
                'name': TEST_GROUP_NAME_EDITED
            }
        )

    def _request_test_group_list_api_view(self):
        return self.get(viewname='rest_api:group-list')


class GroupLinkTestMixin:
    def _resolve_group_setup_link(self):
        self.add_test_view()
        context = self.get_test_view()
        return link_group_setup.resolve(context=context)


class GroupTestMixin:
    def setUp(self):
        super().setUp()
        self._test_group_list = []

    def _create_test_group(self, add_users=None):
        total_test_group_count = len(self._test_group_list)
        name = '{}_{}'.format(TEST_GROUP_NAME, total_test_group_count)

        self._test_group = Group.objects.create(name=name)

        self._test_group_list.append(self._test_group)

        for user in add_users or []:
            self._test_group.user_set.add(user)

    def _edit_test_group(self):
        self._test_group.name = TEST_GROUP_NAME_EDITED
        self._test_group.save()


class GroupUserAPIViewTestMixin:
    def _request_test_group_user_add_api_view(self):
        return self.post(
            viewname='rest_api:group-user-add', kwargs={
                'group_id': self._test_group.pk
            }, data={'user': self._test_user.pk}
        )

    def _request_test_group_user_list_api_view(self):
        return self.get(
            viewname='rest_api:group-user-list', kwargs={
                'group_id': self._test_group.pk
            }
        )

    def _request_test_group_user_remove_api_view(self):
        return self.post(
            viewname='rest_api:group-user-remove', kwargs={
                'group_id': self._test_group.pk
            }, data={'user': self._test_user.pk}
        )


class GroupUserViewTestMixin:
    def _request_test_group_user_add_remove_get_view(self):
        return self.get(
            viewname='user_management:group_members', kwargs={
                'group_id': self._test_group.pk
            }
        )

    def _request_test_group_user_add_view(self):
        return self.post(
            viewname='user_management:group_members', kwargs={
                'group_id': self._test_group.pk
            }, data={
                'available-submit': 'true',
                'available-selection': self._test_user.pk
            }
        )

    def _request_test_group_user_remove_view(self):
        return self.post(
            viewname='user_management:group_members', kwargs={
                'group_id': self._test_group.pk
            }, data={
                'added-submit': 'true',
                'added-selection': self._test_user.pk
            }
        )


class GroupViewTestMixin:
    def _request_test_group_create_view(self):
        response = self.post(
            viewname='user_management:group_create', data={
                'name': TEST_GROUP_NAME
            }
        )
        self._test_group = Group.objects.filter(name=TEST_GROUP_NAME).first()
        return response

    def _request_test_group_single_delete_view(self):
        return self.post(
            viewname='user_management:group_single_delete', kwargs={
                'group_id': self._test_group.pk
            }
        )

    def _request_test_group_multiple_delete_view(self):
        return self.post(
            viewname='user_management:group_multiple_delete', data={
                'id_list': self._test_group.pk
            }
        )

    def _request_test_group_edit_view(self):
        return self.post(
            viewname='user_management:group_edit', kwargs={
                'group_id': self._test_group.pk
            }, data={
                'name': TEST_GROUP_NAME_EDITED
            }
        )

    def _request_test_group_list_view(self):
        return self.get(viewname='user_management:group_list')

    def _request_test_group_members_view(self):
        return self.get(
            viewname='user_management:group_members', kwargs={
                'group_id': self._test_group.pk
            }
        )


class UserAPIViewTestMixin:
    def _request_test_user_create_api_view(self):
        result = self.post(
            viewname='rest_api:user-list', data={
                'email': TEST_USER_EMAIL, 'password': TEST_USER_PASSWORD,
                'username': TEST_USER_USERNAME
            }
        )
        if 'id' in result.json():
            self._test_user = get_user_model().objects.get(
                pk=result.json()['id']
            )

        return result

    def _request_test_user_delete_api_view(self):
        return self.delete(
            viewname='rest_api:user-detail', kwargs={
                'user_id': self._test_user.pk
            }
        )

    def _request_test_user_detail_api_view(self):
        return self.get(
            viewname='rest_api:user-detail', kwargs={
                'user_id': self._test_user.pk
            }
        )

    def _request_test_user_edit_patch_api_view(self):
        return self.patch(
            viewname='rest_api:user-detail', kwargs={
                'user_id': self._test_user.pk
            }, data={'username': TEST_USER_USERNAME_EDITED}
        )

    def _request_test_user_edit_put_api_view(self):
        return self.put(
            viewname='rest_api:user-detail', kwargs={
                'user_id': self._test_user.pk
            }, data={'username': TEST_USER_USERNAME_EDITED}
        )

    def _request_test_user_password_change_api_view(self):
        result = self.patch(
            viewname='rest_api:user-detail', kwargs={
                'user_id': self._test_user.pk
            }, data={
                'password': TEST_USER_PASSWORD_EDITED
            }
        )

        self._test_user.cleartext_password = TEST_USER_PASSWORD_EDITED

        return result


class UserGroupAPIViewTestMixin:
    def _request_test_user_group_list_api_view(self):
        return self.get(
            viewname='rest_api:user-group-list', kwargs={
                'user_id': self._test_user.pk
            }
        )


class UserLinkTestMixin:
    def _resolve_user_setup_link(self):
        self.add_test_view()
        context = self.get_test_view()
        return link_user_setup.resolve(context=context)


class UserTestCaseMixin:
    """
    This TestCaseMixin is used to create a user and group to execute the
    test case, these are used to just create an identity which is required by
    most of the code in the project, these are not meant to be acted upon
    (edited, deleted, etc). To create a test users or groups to modify, use
    the UserTestMixin instead and the respective test_user and test_group.
    The user and group created by this mixin will be prepended with
    _test_case_{...}. The _test_case_user and _test_case_group are meant
    to be used by other test case mixins like the ACLs test case mixin which
    adds shorthand methods to create ACL entries to test access control.
    """
    auto_login_super_user = False
    auto_login_user = True
    create_test_case_super_user = False
    create_test_case_user = True

    def setUp(self):
        super().setUp()
        if self.create_test_case_user:
            self._create_test_case_user()
            self._create_test_case_group()
            self._test_case_group.user_set.add(self._test_case_user)

            if self.auto_login_user:
                self.login_user()

        if self.create_test_case_super_user:
            self._create_test_case_super_user()

            if self.auto_login_super_user:
                self.login_super_user()

    def tearDown(self):
        self.client.logout()
        super().tearDown()

    def _create_test_case_group(self):
        self._test_case_group = Group.objects.create(
            name=TEST_CASE_GROUP_NAME
        )

    def _create_test_case_super_user(self):
        self._test_case_super_user = get_user_model().objects.create_superuser(
            email=TEST_CASE_SUPER_USER_EMAIL,
            password=TEST_CASE_SUPER_USER_PASSWORD,
            username=TEST_CASE_SUPER_USER_USERNAME
        )
        self._test_case_super_user.cleartext_password = TEST_CASE_SUPER_USER_PASSWORD

    def _create_test_case_user(self):
        self._test_case_user = get_user_model().objects.create_user(
            email=TEST_CASE_USER_EMAIL, first_name=TEST_CASE_USER_FIRST_NAME,
            last_name=TEST_CASE_USER_LAST_NAME,
            password=TEST_CASE_USER_PASSWORD,
            username=TEST_CASE_USER_USERNAME
        )
        self._test_case_user.cleartext_password = TEST_CASE_USER_PASSWORD

    def login(self, *args, **kwargs):
        return self.client.login(*args, **kwargs)

    def login_super_user(self):
        return self.login(
            password=TEST_CASE_SUPER_USER_PASSWORD,
            username=TEST_CASE_SUPER_USER_USERNAME
        )

    def login_user(self):
        return self.login(
            password=TEST_CASE_USER_PASSWORD,
            username=TEST_CASE_USER_USERNAME
        )

    def logout(self):
        self.client.logout()


class UserTestMixin:
    auto_create_test_user = False
    auto_create_test_super_user = False

    def setUp(self):
        super().setUp()
        self._test_user_list = []

        if self.auto_create_test_super_user:
            self._create_test_super_user()

        if self.auto_create_test_user:
            self._create_test_user()

    def _create_test_super_user(self):
        self._test_super_user = get_user_model().objects.create_superuser(
            email=TEST_CASE_SUPER_USER_EMAIL,
            password=TEST_CASE_SUPER_USER_PASSWORD,
            username=TEST_CASE_SUPER_USER_USERNAME
        )
        self._test_super_user.cleartext_password = TEST_USER_PASSWORD

    def _create_test_user(self):
        total_test_user_count = len(self._test_user_list)
        username = '{}_{}'.format(TEST_USER_USERNAME, total_test_user_count)

        self._test_user = get_user_model().objects.create_user(
            email=TEST_USER_EMAIL, password=TEST_USER_PASSWORD,
            username=username
        )
        self._test_user.cleartext_password = TEST_USER_PASSWORD
        self._test_user_list.append(self._test_user)


class UserViewTestMixin:
    def _request_test_super_user_delete_view(self):
        return self.post(
            viewname='user_management:user_single_delete',
            kwargs={'user_id': self._test_super_user.pk}
        )

    def _request_test_super_user_detail_view(self):
        return self.get(
            viewname='user_management:user_details',
            kwargs={'user_id': self._test_super_user.pk}
        )

    def _request_test_user_create_view(self):
        response = self.post(
            viewname='user_management:user_create', data={
                'password': TEST_USER_PASSWORD,
                'username': TEST_USER_USERNAME
            }
        )

        self._test_user = get_user_model().objects.filter(
            username=TEST_USER_USERNAME
        ).first()
        return response

    def _request_test_user_single_delete_get_view(self):
        return self.get(
            viewname='user_management:user_single_delete',
            kwargs={'user_id': self._test_user.pk}
        )

    def _request_test_user_single_delete_post_view(self):
        return self.post(
            viewname='user_management:user_single_delete',
            kwargs={'user_id': self._test_user.pk}
        )

    def _request_test_user_multiple_delete_get_view(self):
        return self.get(
            viewname='user_management:user_multiple_delete', data={
                'id_list': self._test_user.pk
            }
        )

    def _request_test_user_multiple_delete_post_view(self):
        return self.post(
            viewname='user_management:user_multiple_delete', data={
                'id_list': self._test_user.pk
            }
        )

    def _request_test_user_detail_view(self):
        return self.get(
            viewname='user_management:user_details', kwargs={
                'user_id': self._test_user.pk
            }
        )

    def _request_test_user_edit_view(self):
        return self.post(
            viewname='user_management:user_edit', kwargs={
                'user_id': self._test_user.pk
            }, data={
                'username': TEST_USER_USERNAME_EDITED
            }
        )

    def _request_test_user_list_view(self):
        return self.get(viewname='user_management:user_list')

    def _request_test_user_options_view(self):
        return self.post(
            viewname='user_management:user_options', kwargs={
                'user_id': self._test_user.pk
            }, data={
                'block_password_change': True
            }
        )


class UserGroupViewTestMixin:
    def _request_test_user_group_add_remove_get_view(self):
        return self.get(
            viewname='user_management:user_groups', kwargs={
                'user_id': self._test_user.pk
            }
        )

    def _request_test_user_group_add_view(self):
        return self.post(
            viewname='user_management:user_groups', kwargs={
                'user_id': self._test_user.pk
            }, data={
                'available-submit': 'true',
                'available-selection': self._test_group.pk
            }
        )

    def _request_test_user_group_remove_view(self):
        return self.post(
            viewname='user_management:user_groups', kwargs={
                'user_id': self._test_user.pk
            }, data={
                'added-submit': 'true',
                'added-selection': self._test_group.pk
            }
        )
