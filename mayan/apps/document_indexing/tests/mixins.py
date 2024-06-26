from mayan.apps.events.classes import EventType
from mayan.apps.testing.tests.mixins import TestMixinObjectCreationTrack

from ..literals import RELATIONSHIP_NO, RELATIONSHIP_YES
from ..models.index_instance_models import IndexInstance
from ..models.index_template_models import IndexTemplate, IndexTemplateNode

from .literals import (
    TEST_INDEX_TEMPLATE_LABEL, TEST_INDEX_TEMPLATE_LABEL_EDITED,
    TEST_INDEX_TEMPLATE_NODE_EXPRESSION,
    TEST_INDEX_TEMPLATE_NODE_EXPRESSION_EDITED, TEST_INDEX_TEMPLATE_SLUG
)


class DocumentIndexAPIViewTestMixin:
    def _request_test_document_index_instance_list_api_view(self):
        return self.get(
            viewname='rest_api:document-index-list', kwargs={
                'document_id': self._test_document.pk
            }
        )


class DocumentIndexInstanceViewTestMixin:
    def _request_test_document_index_instance_list_view(self):
        return self.get(
            viewname='indexing:document_index_list', kwargs={
                'document_id': self._test_document.pk
            }
        )


class DocumentTypeAddRemoveIndexTemplateViewTestMixin:
    def _request_test_document_type_index_template_add_remove_get_view(self):
        return self.get(
            viewname='indexing:document_type_index_templates', kwargs={
                'document_type_id': self._test_document_type.pk
            }
        )

    def _request_test_document_type_index_template_add_view(self):
        return self.post(
            viewname='indexing:document_type_index_templates', kwargs={
                'document_type_id': self._test_document_type.pk
            }, data={
                'available-submit': 'true',
                'available-selection': self._test_index_template.pk
            }
        )

    def _request_test_document_type_index_template_remove_view(self):
        return self.post(
            viewname='indexing:document_type_index_templates', kwargs={
                'document_type_id': self._test_document_type.pk
            }, data={
                'added-submit': 'true',
                'added-selection': self._test_index_template.pk
            }
        )


class IndexInstanceAPIViewTestMixin:
    def _request_test_index_instance_list_api_view(self):
        return self.get(viewname='rest_api:indexinstance-list')

    def _request_test_index_instance_detail_api_view(self):
        return self.get(
            viewname='rest_api:indexinstance-detail', kwargs={
                'index_instance_id': self._test_index_instance.pk
            }
        )


class IndexInstanceNodeAPIViewTestMixin:
    def _request_test_index_instance_node_children_list_api_view(self):
        return self.get(
            viewname='rest_api:indexinstancenode-children-list', kwargs={
                'index_instance_id': self._test_index_instance.pk,
                'index_instance_node_id': self._test_index_instance_node.pk
            }
        )

    def _request_test_index_instance_node_detail_api_view(self):
        return self.get(
            viewname='rest_api:indexinstancenode-detail', kwargs={
                'index_instance_id': self._test_index_instance.pk,
                'index_instance_node_id': self._test_index_instance_node.pk
            }
        )

    def _request_test_index_instance_node_document_list_api_view(self):
        return self.get(
            viewname='rest_api:indexinstancenode-document-list', kwargs={
                'index_instance_id': self._test_index_instance.pk,
                'index_instance_node_id': self._test_index_instance_node.pk
            }
        )

    def _request_test_index_instance_node_list_api_view(self):
        return self.get(
            viewname='rest_api:indexinstancenode-list', kwargs={
                'index_instance_id': self._test_index_instance.pk
            }
        )


class IndexInstanceTestMixin:
    def setUp(self):
        super().setUp()
        self._test_index_instance = IndexInstance.objects.get(
            pk=self._test_index_template.pk
        )

    def _populate_test_index_instance_node(self):
        self._test_index_instance_root_node = self._test_index_instance.index_instance_root_node
        self._test_index_instance_node = self._test_index_instance_root_node.get_children().first()


class IndexInstanceViewTestMixin:
    def _request_test_index_instance_node_view(self, index_instance_node):
        return self.get(
            viewname='indexing:index_instance_node_view', kwargs={
                'index_instance_node_id': index_instance_node.pk
            }
        )


class IndexTemplateNodeViewTestMixin:
    def _request_test_index_template_node_create_view(self):
        return self.post(
            viewname='indexing:template_node_create', kwargs={
                'index_template_node_id': self._test_index_template.index_template_root_node.pk
            }, data={
                'expression_template': TEST_INDEX_TEMPLATE_NODE_EXPRESSION,
                'index': self._test_index_template.pk,
                'link_document': True
            }
        )

    def _request_test_index_template_node_delete_view(self):
        return self.post(
            viewname='indexing:template_node_delete', kwargs={
                'index_template_node_id': self._test_index_template_node.pk
            }
        )

    def _request_test_index_template_node_edit_view(self):
        return self.post(
            viewname='indexing:template_node_edit', kwargs={
                'index_template_node_id': self._test_index_template_node.pk
            }, data={
                'expression_template': TEST_INDEX_TEMPLATE_NODE_EXPRESSION_EDITED,
                'index': self._test_index_template.pk
            }
        )

    def _request_test_index_template_node_list_view(self):
        return self.get(
            viewname='indexing:index_template_view', kwargs={
                'index_template_id': self._test_index_template.pk
            }
        )


class IndexTemplateTestMixin(TestMixinObjectCreationTrack):
    _test_index_template_node_expression = None
    _test_object_model = IndexTemplate
    _test_object_name = '_test_index_template'
    auto_add_test_index_template_to_test_document_type = True
    auto_create_test_index_template = True
    auto_create_test_index_template_node = True

    def setUp(self):
        super().setUp()

        EventType.refresh()

        self._test_index_template_list = []
        self._test_index_template_data = [
            {
                'label': TEST_INDEX_TEMPLATE_LABEL,
                'slug': TEST_INDEX_TEMPLATE_SLUG
            },
            {
                'label': '{}_1'.format(TEST_INDEX_TEMPLATE_LABEL),
                'slug': '{}_1'.format(TEST_INDEX_TEMPLATE_SLUG)
            }
        ]

        if self.auto_create_test_index_template:
            self._create_test_index_template(
                add_test_document_type=self.auto_add_test_index_template_to_test_document_type
            )
            if self.auto_create_test_index_template_node:
                self._create_test_index_template_node(
                    expression=self._test_index_template_node_expression
                )

    def _create_test_index_template(
        self, add_test_document_type=False, extra_data=None
    ):
        data = self._test_index_template_data[
            len(self._test_index_template_list)
        ]

        if extra_data:
            data.update(extra_data)

        # Create empty index.
        self._test_index_template = IndexTemplate.objects.create(**data)

        self._test_index_template_list.append(self._test_index_template)

        self._test_index_template_root_node = self._test_index_template.index_template_root_node

        if add_test_document_type:
            self._test_index_template.document_types.add(
                self._test_document_type
            )

        self._test_index_template.event_triggers.filter(
            stored_event_type__name__startswith='acls'
        ).delete()

    def _create_test_index_template_node(
        self, expression=None, link_documents=True, rebuild=False
    ):
        expression = expression or TEST_INDEX_TEMPLATE_NODE_EXPRESSION

        self._test_index_template_node = self._test_index_template.index_template_nodes.create(
            parent=self._test_index_template.index_template_root_node,
            expression=expression, link_documents=link_documents
        )

        if rebuild:
            self._rebuild_test_index_template()


class IndexTemplateActionAPIViewTestMixin:
    def _request_test_index_template_rebuild_api_view(self):
        return self.post(
            viewname='rest_api:indextemplate-rebuild', kwargs={
                'index_template_id': self._test_index_template.pk
            }
        )

    def _request_test_index_template_reset_api_view(self):
        return self.post(
            viewname='rest_api:indextemplate-reset', kwargs={
                'index_template_id': self._test_index_template.pk
            }
        )


class IndexTemplateAPIViewTestMixin(IndexTemplateTestMixin):
    def _request_test_index_template_create_api_view(self):
        self._test_object_track()

        response = self.post(
            viewname='rest_api:indextemplate-list', data={
                'label': TEST_INDEX_TEMPLATE_LABEL,
                'slug': TEST_INDEX_TEMPLATE_SLUG
            }
        )

        self._test_object_set()

        return response

    def _request_test_index_template_delete_api_view(self):
        return self.delete(
            viewname='rest_api:indextemplate-detail', kwargs={
                'index_template_id': self._test_index_template.pk
            }
        )

    def _request_test_index_template_detail_api_view(self):
        return self.get(
            viewname='rest_api:indextemplate-detail', kwargs={
                'index_template_id': self._test_index_template.pk
            }
        )

    def _request_test_index_template_edit_via_patch_api_view(self):
        return self.patch(
            viewname='rest_api:indextemplate-detail', kwargs={
                'index_template_id': self._test_index_template.pk
            }, data={'label': TEST_INDEX_TEMPLATE_LABEL_EDITED}
        )

    def _request_test_index_template_list_api_view(self):
        return self.get(viewname='rest_api:indextemplate-list')


class IndexTemplateDocumentTypeAPIViewTestMixin:
    def _request_test_index_template_document_type_list_api_view(self):
        return self.get(
            viewname='rest_api:indextemplate-documenttype-list', kwargs={
                'index_template_id': self._test_index_template.pk
            }
        )

    def _request_test_index_template_document_type_add_api_view(self):
        return self.post(
            viewname='rest_api:indextemplate-documenttype-add', kwargs={
                'index_template_id': self._test_index_template.pk
            }, data={
                'document_type': self._test_document_type.pk
            }
        )

    def _request_test_index_template_document_type_remove_api_view(self):
        return self.post(
            viewname='rest_api:indextemplate-documenttype-remove', kwargs={
                'index_template_id': self._test_index_template.pk
            }, data={
                'document_type': self._test_document_type.pk
            }
        )


class IndexTemplateEventTriggerViewTestMixin:
    def _request_test_index_template_event_trigger_get_view(self):
        return self.get(
            viewname='indexing:index_template_event_triggers',
            kwargs={
                'index_template_id': self._test_index_template.pk
            }
        )

    def _request_test_index_template_event_trigger_add_view(
        self, stored_event_type_id
    ):
        data = {
            'form-INITIAL_FORMS': '0',
            'form-TOTAL_FORMS': '1',
            'form-0-relationship': RELATIONSHIP_YES,
            'form-0-stored_event_type_id': stored_event_type_id
        }

        return self.post(
            viewname='indexing:index_template_event_triggers',
            kwargs={
                'index_template_id': self._test_index_template.pk
            }, data=data
        )

    def _request_test_index_template_event_trigger_remove_view(
        self, stored_event_type_id
    ):
        data = {
            'form-INITIAL_FORMS': '0',
            'form-TOTAL_FORMS': '1',
            'form-0-relationship': RELATIONSHIP_NO,
            'form-0-stored_event_type_id': stored_event_type_id
        }

        return self.post(
            viewname='indexing:index_template_event_triggers',
            kwargs={
                'index_template_id': self._test_index_template.pk
            }, data=data
        )


class IndexTemplateNodeAPITestMixin:
    def _request_test_index_template_node_create_api_view(
        self, extra_data=None
    ):
        data = {
            'expression': TEST_INDEX_TEMPLATE_NODE_EXPRESSION
        }

        if extra_data:
            data.update(extra_data)

        values = list(
            IndexTemplateNode.objects.values_list('pk', flat=True)
        )

        response = self.post(
            viewname='rest_api:indextemplatenode-list', kwargs={
                'index_template_id': self._test_index_template.pk
            }, data=data
        )
        self._test_index_template_node = IndexTemplateNode.objects.exclude(
            pk__in=values
        ).first()

        return response

    def _request_test_index_template_node_delete_api_view(self):
        return self.delete(
            viewname='rest_api:indextemplatenode-detail', kwargs={
                'index_template_id': self._test_index_template.pk,
                'index_template_node_id': self._test_index_template_node.pk
            }
        )

    def _request_test_index_template_node_detail_api_view(self):
        return self.get(
            viewname='rest_api:indextemplatenode-detail', kwargs={
                'index_template_id': self._test_index_template.pk,
                'index_template_node_id': self._test_index_template_node.pk
            }
        )

    def _request_test_index_template_node_edit_via_patch_api_view(
        self, extra_data=None
    ):
        data = {
            'enabled': self._test_index_template_node.enabled,
            'expression': self._test_index_template_node.expression,
            'index': self._test_index_template.pk,
            'link_documents': self._test_index_template_node.link_documents,
            'parent': self._test_index_template_node.parent.pk
        }
        data['expression'] = TEST_INDEX_TEMPLATE_NODE_EXPRESSION_EDITED

        if extra_data:
            data.update(**extra_data)

        return self.patch(
            viewname='rest_api:indextemplatenode-detail', kwargs={
                'index_template_id': self._test_index_template.pk,
                'index_template_node_id': self._test_index_template_node.pk
            }, data=data
        )

    def _request_test_index_template_node_list_api_view(self):
        return self.get(
            viewname='rest_api:indextemplatenode-list', kwargs={
                'index_template_id': self._test_index_template.pk
            }
        )


class IndexToolsViewTestMixin:
    def _request_index_all_rebuild_get_view(self):
        return self.get(
            viewname='indexing:rebuild_index_instances'
        )

    def _request_indexes_rebuild_post_view(self):
        return self.post(
            viewname='indexing:rebuild_index_instances', data={
                'index_templates': self._test_index_template.pk
            }
        )

    def _request_index_all_reset_get_view(self):
        return self.get(
            viewname='indexing:index_instances_reset'
        )

    def _request_index_all_reset_post_view(self):
        return self.post(
            viewname='indexing:index_instances_reset', data={
                'index_templates': self._test_index_template.pk
            }
        )


class IndexTemplateViewTestMixin:
    def _request_test_index_template_create_view(self):
        self._test_object_track()

        response = self.post(
            viewname='indexing:index_template_create', data={
                'label': TEST_INDEX_TEMPLATE_LABEL,
                'slug': TEST_INDEX_TEMPLATE_SLUG
            }
        )

        self._test_object_set()

        return response

    def _request_test_index_template_delete_view(self):
        return self.post(
            viewname='indexing:index_template_delete', kwargs={
                'index_template_id': self._test_index_template.pk
            }
        )

    def _request_test_index_template_document_type_add_remove_get_view(self):
        return self.get(
            viewname='indexing:index_template_document_types', kwargs={
                'index_template_id': self._test_index_template.pk
            }
        )

    def _request_test_index_template_document_type_add_view(self):
        return self.post(
            viewname='indexing:index_template_document_types', kwargs={
                'index_template_id': self._test_index_template.pk
            }, data={
                'available-submit': 'true',
                'available-selection': self._test_document_type.pk
            }
        )

    def _request_test_index_template_document_type_remove_view(self):
        return self.post(
            viewname='indexing:index_template_document_types', kwargs={
                'index_template_id': self._test_index_template.pk
            }, data={
                'added-submit': 'true',
                'added-selection': self._test_document_type.pk
            }
        )

    def _request_test_index_template_edit_view(self):
        return self.post(
            viewname='indexing:index_template_edit', kwargs={
                'index_template_id': self._test_index_template.pk
            }, data={
                'label': TEST_INDEX_TEMPLATE_LABEL_EDITED,
                'slug': TEST_INDEX_TEMPLATE_SLUG
            }
        )

    def _request_test_index_template_rebuild_view(self):
        return self.post(
            viewname='indexing:index_template_rebuild', kwargs={
                'index_template_id': self._test_index_template.pk
            }
        )
