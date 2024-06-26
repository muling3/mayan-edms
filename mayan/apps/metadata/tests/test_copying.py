from mayan.apps.common.tests.mixins import ObjectCopyTestMixin
from mayan.apps.documents.tests.mixins.document_mixins import (
    DocumentTestMixin
)
from mayan.apps.testing.tests.base import BaseTestCase

from .mixins.metadata_type_mixins import MetadataTypeTestMixin


class MetadataTypeCopyTestCase(
    DocumentTestMixin, MetadataTypeTestMixin, ObjectCopyTestMixin,
    BaseTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_metadata_type()
        self._test_metadata_type.document_types.create(
            document_type=self._test_document_type
        )
        self._test_object = self._test_metadata_type
