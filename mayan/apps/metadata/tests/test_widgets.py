from mayan.apps.documents.permissions import (
    permission_document_file_view, permission_document_version_view,
    permission_document_view
)
from mayan.apps.documents.search import (
    search_model_document, search_model_document_file,
    search_model_document_file_page, search_model_document_version,
    search_model_document_version_page
)
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.dynamic_search.literals import SEARCH_MODEL_NAME_KWARG
from mayan.apps.dynamic_search.tests.mixins.search_view_mixins import (
    SearchViewTestMixin
)

from ..permissions import permission_document_metadata_view

from .mixins.document_metadata_mixins import DocumentMetadataMixin


class DocumentSearchResultWidgetViewTestCase(
    DocumentMetadataMixin, SearchViewTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_metadata_type(add_test_document_type=True)
        self._upload_test_document()
        self._create_test_document_metadata()
        self._test_object_permission = permission_document_view
        self._test_object_text = self._test_document.label
        self._test_search_model = search_model_document
        self._test_search_term_data = {
            'uuid': str(self._test_document.uuid)
        }

    def test_document_metadata_widget_no_permission(self):
        response = self._request_search_results_view(
            data=self._test_search_term_data, kwargs={
                SEARCH_MODEL_NAME_KWARG: self._test_search_model.full_name
            }
        )
        self.assertNotContains(
            response=response, text=self._test_object_text,
            status_code=200
        )
        self.assertNotContains(
            response=response, text=self._test_metadata_type.label,
            status_code=200
        )

    def test_document_metadata_widget_with_metadata_type_access(self):
        self.grant_access(
            obj=self._test_metadata_type,
            permission=permission_document_metadata_view
        )

        response = self._request_search_results_view(
            data=self._test_search_term_data, kwargs={
                SEARCH_MODEL_NAME_KWARG: self._test_search_model.full_name
            }
        )
        self.assertNotContains(
            response=response, text=self._test_object_text, status_code=200
        )
        self.assertNotContains(
            response=response, text=self._test_metadata_type.label,
            status_code=200
        )

    def test_document_metadata_widget_with_document_view_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=self._test_object_permission
        )

        response = self._request_search_results_view(
            data=self._test_search_term_data, kwargs={
                SEARCH_MODEL_NAME_KWARG: self._test_search_model.full_name
            }
        )
        self.assertContains(
            response=response, text=self._test_object_text, status_code=200
        )
        self.assertNotContains(
            response=response, text=self._test_metadata_type.label,
            status_code=200
        )

    def test_document_metadata_widget_with_document_metadata_view_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_metadata_view
        )

        response = self._request_search_results_view(
            data=self._test_search_term_data, kwargs={
                SEARCH_MODEL_NAME_KWARG: self._test_search_model.full_name
            }
        )
        self.assertNotContains(
            response=response, text=self._test_object_text, status_code=200
        )
        self.assertNotContains(
            response=response, text=self._test_metadata_type.label,
            status_code=200
        )

    def test_document_metadata_widget_with_all_document_access(self):
        self.grant_access(
            obj=self._test_document, permission=self._test_object_permission
        )
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_metadata_view
        )

        response = self._request_search_results_view(
            data=self._test_search_term_data, kwargs={
                SEARCH_MODEL_NAME_KWARG: self._test_search_model.full_name
            }
        )
        self.assertContains(
            response=response, text=self._test_object_text, status_code=200
        )
        self.assertNotContains(
            response=response, text=self._test_metadata_type.label,
            status_code=200
        )

    def test_document_metadata_widget_with_metadata_view_and_document_view_access(self):
        self.grant_access(
            obj=self._test_document, permission=self._test_object_permission
        )
        self.grant_access(
            obj=self._test_metadata_type,
            permission=permission_document_metadata_view
        )

        response = self._request_search_results_view(
            data=self._test_search_term_data, kwargs={
                SEARCH_MODEL_NAME_KWARG: self._test_search_model.full_name
            }
        )
        self.assertContains(
            response=response, text=self._test_object_text, status_code=200
        )
        self.assertNotContains(
            response=response, text=self._test_metadata_type.label,
            status_code=200
        )

    def test_document_metadata_widget_with_full_access(self):
        self.grant_access(
            obj=self._test_document, permission=self._test_object_permission
        )
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_metadata_view
        )
        self.grant_access(
            obj=self._test_metadata_type,
            permission=permission_document_metadata_view
        )

        response = self._request_search_results_view(
            data=self._test_search_term_data, kwargs={
                SEARCH_MODEL_NAME_KWARG: self._test_search_model.full_name
            }
        )
        self.assertContains(
            response=response, text=self._test_object_text, status_code=200
        )
        self.assertContains(
            response=response, text=self._test_metadata_type.label,
            status_code=200
        )


class DocumentFileSearchResultWidgetViewTestCase(
    DocumentSearchResultWidgetViewTestCase
):
    def setUp(self):
        super().setUp()
        self._test_object_text = self._test_document_file.filename
        self._test_object_permission = permission_document_file_view
        self._test_search_model = search_model_document_file
        self._test_search_term_data = {
            'document__uuid': str(self._test_document.uuid)
        }


class DocumentFilePageSearchResultWidgetViewTestCase(
    DocumentSearchResultWidgetViewTestCase
):
    def setUp(self):
        super().setUp()
        self._test_object_text = str(
            self._test_document_file.pages.first()
        )
        self._test_object_permission = permission_document_file_view
        self._test_search_model = search_model_document_file_page
        self._test_search_term_data = {
            'document_file__document__uuid': str(self._test_document.uuid)
        }


class DocumentVersionSearchResultWidgetViewTestCase(
    DocumentSearchResultWidgetViewTestCase
):
    def setUp(self):
        super().setUp()
        self._test_object_text = str(self._test_document_version)
        self._test_object_permission = permission_document_version_view
        self._test_search_model = search_model_document_version
        self._test_search_term_data = {
            'document__uuid': str(self._test_document.uuid)
        }


class DocumentVersionPageSearchResultWidgetViewTestCase(
    DocumentSearchResultWidgetViewTestCase
):
    def setUp(self):
        super().setUp()
        self._test_object_text = str(
            self._test_document_version.pages.first()
        )
        self._test_object_permission = permission_document_version_view
        self._test_search_model = search_model_document_version_page
        self._test_search_term_data = {
            'document_version__document__uuid': str(self._test_document.uuid)
        }
