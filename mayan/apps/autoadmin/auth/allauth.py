"""
Authentication adapters for Allauth
"""
try:
    from allauth.account.adapter import DefaultAccountAdapter
except ImportError:
    print('ERROR: This authentication adapter requires django-allauth.')
    raise

from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from .literals import ADMIN_EMAIL_ADDRESSES


class AutoadminAccountAdapter(DefaultAccountAdapter):
    """
    Allauth account adapter that enables automatic grant of admin permissions
    to users signing up having their email address listed in the ``ADMINS``
    Django settings.  Django settings needed to activate this feature:

        INSTALLED_APPS = [
            'django.contrib.auth',
            'django.contrib.sites',
            'allauth',
            'allauth.account',
            'allauth.socialaccount',
        ]

        ACCOUNT_ADAPTER = 'autoadmin.auth.allauth.AutoadminAccountAdapter'

    See also:
    - http://django-allauth.readthedocs.io/en/latest/configuration.html
    - http://django-allauth.readthedocs.io/en/latest/advanced.html#admin
    """

    def confirm_email(self, request, email_address):
        """
        Give super user privileges automagically if the email address of a
        user confirming their email is listed in ``settings.ADMINS``.
        """
        super().confirm_email(request=request, email_address=email_address)

        if email_address.email in ADMIN_EMAIL_ADDRESSES:
            user = email_address.user
            user.is_staff = user.is_superuser = True
            user.save()

            messages.info(
                request=request, message=_(
                    message='Welcome Admin! You have been given super user '
                    'privileges. Use them with caution.'
                )
            )
