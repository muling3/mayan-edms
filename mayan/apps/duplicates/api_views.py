from mayan.apps.documents.api_views.api_view_mixins import (
    ParentObjectDocumentAPIViewMixin
)
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.serializers.document_serializers import (
    DocumentSerializer
)
from mayan.apps.rest_api import generics

from .models import DuplicateBackendEntry
from .serializers import DuplicateTargetDocumentSerializer


class APIDuplicatedDocumentListView(generics.ListAPIView):
    """
    get: Return a list of duplicated documents.
    """
    mayan_object_permission_map = {'GET': permission_document_view}
    serializer_class = DocumentSerializer
    source_queryset = DuplicateBackendEntry.objects.get_duplicated_documents()


class APIDocumentDuplicateListView(
    ParentObjectDocumentAPIViewMixin, generics.ListAPIView
):
    """
    get: Return a list of the selected document's duplicates.
    """
    mayan_object_permission_map = {'GET': permission_document_view}
    serializer_class = DuplicateTargetDocumentSerializer

    def get_source_queryset(self):
        return DuplicateBackendEntry.objects.get_duplicates_of(
            document=self.get_document(
                permission=permission_document_view
            )
        )
