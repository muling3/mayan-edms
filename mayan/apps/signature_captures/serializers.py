from django.utils.translation import gettext_lazy as _

from mayan.apps.rest_api import serializers
from mayan.apps.rest_api.relations import MultiKwargHyperlinkedIdentityField

from .models import SignatureCapture


class SignatureCaptureSerializer(serializers.HyperlinkedModelSerializer):
    document_url = serializers.HyperlinkedIdentityField(
        label=_(message='Document URL'), lookup_field='document_id',
        lookup_url_kwarg='document_id', view_name='rest_api:document-detail'
    )
    image_url = MultiKwargHyperlinkedIdentityField(
        label=_(message='Image URL'), view_kwargs=(
            {
                'lookup_field': 'document_id',
                'lookup_url_kwarg': 'document_id'
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'signature_capture_id'
            }
        ), view_name='rest_api:signature_capture-image'
    )
    url = MultiKwargHyperlinkedIdentityField(
        label=_(message='URL'), view_kwargs=(
            {
                'lookup_field': 'document_id',
                'lookup_url_kwarg': 'document_id'
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'signature_capture_id'
            }
        ), view_name='rest_api:signature_capture-detail'
    )

    class Meta:
        fields = (
            'data', 'document_id', 'document_url', 'id', 'image_url',
            'internal_name', 'text', 'url'
        )
        model = SignatureCapture
        read_only_fields = (
            'document_id', 'document_url', 'id', 'image_url', 'url'
        )
