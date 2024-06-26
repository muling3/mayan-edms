from django.utils.translation import gettext_lazy as _

from mayan.apps.smart_settings.settings import setting_cluster

from .literals import (
    DEFAULT_SIGNATURE_CAPTURES_SIGNATURE_CAPTURE_CACHE_MAXIMUM_SIZE,
    DEFAULT_SIGNATURE_CAPTURES_SIGNATURE_CAPTURE_CACHE_STORAGE_BACKEND,
    DEFAULT_SIGNATURE_CAPTURES_SIGNATURE_CAPTURE_CACHE_STORAGE_BACKEND_ARGUMENTS
)
from .setting_callbacks import callback_update_signature_capture_cache_size

setting_namespace = setting_cluster.do_namespace_add(
    label=_(message='Signature captures'), name='signature_captures',
)


setting_signature_capture_cache_maximum_size = setting_namespace.do_setting_add(
    default=DEFAULT_SIGNATURE_CAPTURES_SIGNATURE_CAPTURE_CACHE_MAXIMUM_SIZE,
    global_name='SIGNATURE_CAPTURES_SIGNATURE_CAPTURE_CACHE_MAXIMUM_SIZE',
    help_text=_(
        message='The threshold at which the SIGNATURE_CAPTURES_SIGNATURE_CAPTURE_CACHE_STORAGE_BACKEND '
        'will start deleting the oldest signature capture cache files. '
        'Specify the size in bytes.'
    ), post_edit_function=callback_update_signature_capture_cache_size
)
setting_signature_capture_cache_storage_backend = setting_namespace.do_setting_add(
    default=DEFAULT_SIGNATURE_CAPTURES_SIGNATURE_CAPTURE_CACHE_STORAGE_BACKEND,
    global_name='SIGNATURE_CAPTURES_SIGNATURE_CAPTURE_CACHE_STORAGE_BACKEND',
    help_text=_(
        message='Path to the Storage subclass to use when storing the cached '
        'signature capture files.'
    )
)
setting_signature_capture_cache_storage_backend_arguments = setting_namespace.do_setting_add(
    default=DEFAULT_SIGNATURE_CAPTURES_SIGNATURE_CAPTURE_CACHE_STORAGE_BACKEND_ARGUMENTS,
    global_name='SIGNATURE_CAPTURES_SIGNATURE_CAPTURE_CACHE_STORAGE_BACKEND_ARGUMENTS',
    help_text=_(
        message='Arguments to pass to the SIGNATURE_CAPTURES_SIGNATURE_CAPTURE_CACHE_STORAGE_BACKEND.'
    )
)
