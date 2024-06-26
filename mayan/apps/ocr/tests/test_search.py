from mayan.apps.documents.permissions import (
    permission_document_version_view, permission_document_view
)
from mayan.apps.documents.search import (
    search_model_document, search_model_document_version,
    search_model_document_version_page
)
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.dynamic_search.tests.mixins.base import SearchTestMixin

from .mixins import DocumentVersionOCRTestMixin


class DocumentOCRSearchTestCase(
    DocumentVersionOCRTestMixin, SearchTestMixin, GenericDocumentViewTestCase
):
    _test_search_model = search_model_document
    auto_create_test_document_version_ocr_content = True

    def test_search_model_document_no_permission(self):
        self._clear_events()

        saved_resultset, queryset = self._do_test_search(
            query={
                'versions__version_pages__ocr_content__content': self._test_document_version_page.ocr_content.content
            }
        )
        self.assertTrue(self._test_document not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_model_document_with_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self._clear_events()

        saved_resultset, queryset = self._do_test_search(
            query={
                'versions__version_pages__ocr_content__content': self._test_document_version_page.ocr_content.content
            }
        )
        self.assertTrue(self._test_document in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_search_model_document_with_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self._test_document.delete()

        self._clear_events()

        saved_resultset, queryset = self._do_test_search(
            query={
                'versions__version_pages__ocr_content__content': self._test_document_version_page.ocr_content.content
            }
        )
        self.assertTrue(self._test_document not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class DocumentVersionOCRSearchTestCase(
    DocumentVersionOCRTestMixin, SearchTestMixin, GenericDocumentViewTestCase
):
    _test_search_model = search_model_document_version
    auto_create_test_document_version_ocr_content = True

    def test_search_model_document_version_no_permission(self):
        self._clear_events()

        saved_resultset, queryset = self._do_test_search(
            query={
                'version_pages__ocr_content__content': self._test_document_version_page.ocr_content.content
            }
        )
        self.assertTrue(self._test_document_version not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_model_document_version_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_version_view
        )

        self._clear_events()

        saved_resultset, queryset = self._do_test_search(
            query={
                'version_pages__ocr_content__content': self._test_document_version_page.ocr_content.content
            }
        )
        self.assertTrue(self._test_document_version in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_search_model_document_version_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_version_view
        )

        self._test_document.delete()

        self._clear_events()

        saved_resultset, queryset = self._do_test_search(
            query={
                'version_pages__ocr_content__content': self._test_document_version_page.ocr_content.content
            }
        )
        self.assertTrue(self._test_document_version not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class DocumentVersionPageOCRSearchTestCase(
    DocumentVersionOCRTestMixin, SearchTestMixin, GenericDocumentViewTestCase
):
    _test_search_model = search_model_document_version_page
    auto_create_test_document_version_ocr_content = True

    def test_search_model_document_version_no_permission(self):
        self._clear_events()

        saved_resultset, queryset = self._do_test_search(
            query={
                'ocr_content__content': self._test_document_version_page.ocr_content.content
            }
        )
        self.assertTrue(self._test_document_version_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_model_document_version_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_version_view
        )

        self._clear_events()

        saved_resultset, queryset = self._do_test_search(
            query={
                'ocr_content__content': self._test_document_version_page.ocr_content.content
            }
        )
        self.assertTrue(self._test_document_version_page in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_search_model_document_version_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_version_view
        )

        self._test_document.delete()

        self._clear_events()

        saved_resultset, queryset = self._do_test_search(
            query={
                'ocr_content__content': self._test_document_version_page.ocr_content.content
            }
        )
        self.assertTrue(self._test_document_version_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
