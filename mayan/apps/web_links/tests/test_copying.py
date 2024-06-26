from mayan.apps.common.tests.mixins import ObjectCopyTestMixin
from mayan.apps.documents.tests.mixins.document_mixins import (
    DocumentTestMixin
)
from mayan.apps.testing.tests.base import BaseTestCase

from .mixins import WebLinkTestMixin


class WebLinkCopyTestCase(
    DocumentTestMixin, WebLinkTestMixin, ObjectCopyTestMixin, BaseTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_web_link()
        self._test_web_link.document_types.add(self._test_document_type)
        self._test_object = self._test_web_link
