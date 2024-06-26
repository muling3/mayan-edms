import pyotp

from django.contrib import messages
from django.core.signing import BadSignature, dumps, loads
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView

from mayan.apps.views.generics import (
    ConfirmView, FormView, SingleObjectDetailView
)
from mayan.apps.views.http import URL

from .forms import FormUserOTPDataDetail, FormUserOTPDataEdit
from .view_mixins import OTPBackendEnabledViewMixin


class UserOTPDataDetailView(
    OTPBackendEnabledViewMixin, SingleObjectDetailView
):
    form_class = FormUserOTPDataDetail

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _(
                message='One time pad details for user: %s'
            ) % self.object
        }

    def get_object(self):
        return self.request.user


class UserOTPDataDisableView(OTPBackendEnabledViewMixin, ConfirmView):
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request=request, *args, **kwargs)

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _(
                message='Disable one time pad for user: %s'
            ) % self.object
        }

    def get_object(self):
        return self.request.user

    def view_action(self):
        self.request.user.otp_data.disable()

        messages.success(
            message=_(message='OTP disable successfully.'), request=self.request
        )


class UserOTPDataEnableView(OTPBackendEnabledViewMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        signed_secret = dumps(
            obj=pyotp.random_base32()
        )

        return URL(
            path=reverse(viewname='authentication_otp:otp_verify'),
            query={'signed_secret': signed_secret}
        ).to_string()


class UserOTPDataVerifyTokenView(OTPBackendEnabledViewMixin, FormView):
    form_class = FormUserOTPDataEdit

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.user.otp_data.is_enabled():
            messages.info(
                message=_(message='OTP is already enabled.'),
                request=self.request
            )
            return HttpResponseRedirect(
                redirect_to=reverse(
                    viewname='authentication_otp:otp_detail'
                )
            )
        else:
            return super().dispatch(request=request, *args, **kwargs)

    def form_valid(self, form):
        secret = form.cleaned_data['secret']
        token = form.cleaned_data['token']
        self.request.user.otp_data.enable(secret=secret, token=token)

        messages.success(
            message=_(message='OTP enabled successfully.'),
            request=self.request
        )

        return super().form_valid(form=form)

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _(
                message='Enable one time pad for user: %s'
            ) % self.object
        }

    def get_form_extra_kwargs(self):
        signed_secret = self.request.GET.get('signed_secret', '')

        try:
            secret = loads(s=signed_secret)
        except BadSignature:
            messages.error(
                message=_(
                    message='OTP secret validation error.'
                ), request=self.request
            )
            secret = None

        return {
            'initial': {
                'secret': secret,
                'signed_secret': signed_secret
            },
            'user': self.request.user
        }

    def get_object(self):
        return self.request.user
