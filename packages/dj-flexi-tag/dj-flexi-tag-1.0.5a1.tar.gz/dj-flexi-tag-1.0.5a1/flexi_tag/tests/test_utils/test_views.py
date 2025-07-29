try:
    from unittest import mock
except ImportError:
    import mock

from django.db import models
from django.test import TestCase
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from flexi_tag.exceptions import (
    ObjectIDsNotDefinedException,
    TagNotDefinedException,
    TagNotFoundException,
)
from flexi_tag.utils.models import FlexiTagMixin
from flexi_tag.utils.views import TaggableViewSetMixin


class TaggableTestModel(FlexiTagMixin):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = "tests"


class TestViewSet(TaggableViewSetMixin, ModelViewSet):
    queryset = TaggableTestModel.objects.all()


class TaggableViewSetMixinTestCase(TestCase):
    def setUp(self):
        self.viewset = TestViewSet()
        self.viewset.format_kwarg = None
        self.viewset.taggable_service = mock.MagicMock()
        self.mock_object = mock.MagicMock(spec=TaggableTestModel)
        self.viewset.get_object = mock.MagicMock(return_value=self.mock_object)

        self.mock_queryset = mock.MagicMock()
        self.mock_filtered_queryset = mock.MagicMock()
        self.mock_queryset.filter.return_value = self.mock_filtered_queryset
        self.viewset.get_queryset = mock.MagicMock(return_value=self.mock_queryset)

        self.viewset.paginate_queryset = mock.MagicMock(return_value=None)

        mock_serializer = mock.MagicMock()
        mock_serializer.data = {"data": "serialized_data"}
        self.viewset.get_serializer = mock.MagicMock(return_value=mock_serializer)

    def test_add_tag(self):
        mock_request = mock.MagicMock()
        mock_request.data = {"key": "test_tag"}

        response = self.viewset.add_tag(mock_request, pk=1)

        self.viewset.taggable_service.add_tag.assert_called_once_with(
            instance=self.mock_object,
            key="test_tag",
        )

        self.assertEqual(response.status_code, 200)

    def test_add_tag_missing_key(self):
        mock_request = mock.MagicMock()
        mock_request.data = {}

        with self.assertRaises(TagNotDefinedException):
            self.viewset.add_tag(mock_request, pk=1)

    def test_bulk_add_tag(self):
        mock_request = mock.MagicMock()
        mock_request.data = {"keys": ["tag1", "tag2"]}

        response = self.viewset.bulk_add_tag(mock_request, pk=1)

        self.viewset.taggable_service.bulk_add_tags.assert_called_once_with(
            instance=self.mock_object,
            keys=["tag1", "tag2"],
        )

        self.assertEqual(response.status_code, 200)

    def test_bulk_add_tag_missing_keys(self):
        mock_request = mock.MagicMock()
        mock_request.data = {}

        with self.assertRaises(TagNotDefinedException):
            self.viewset.bulk_add_tag(mock_request, pk=1)

    def test_bulk_add_tags(self):
        mock_request = mock.MagicMock()
        mock_request.data = {"objects": [1, 2], "keys": ["tag1", "tag2"]}

        response = self.viewset.bulk_add_tags(mock_request)

        self.mock_queryset.filter.assert_called_once_with(id__in=[1, 2])

        self.viewset.taggable_service.bulk_add_tags_with_many_instances.assert_called_once_with(
            instances=self.mock_filtered_queryset,
            keys=["tag1", "tag2"],
        )

        self.assertEqual(response.status_code, 200)

    def test_bulk_add_tags_missing_keys(self):
        mock_request = mock.MagicMock()
        mock_request.data = {"objects": [1, 2]}

        with self.assertRaises(TagNotDefinedException):
            self.viewset.bulk_add_tags(mock_request)

    def test_bulk_add_tags_missing_objects(self):
        mock_request = mock.MagicMock()
        mock_request.data = {"keys": ["tag1", "tag2"]}

        with self.assertRaises(ObjectIDsNotDefinedException):
            self.viewset.bulk_add_tags(mock_request)

    def test_remove_tag(self):
        mock_request = mock.MagicMock()
        mock_request.data = {"key": "test_tag"}

        response = self.viewset.remove_tag(mock_request, pk=1)

        self.viewset.taggable_service.remove_tag.assert_called_once_with(
            instance=self.mock_object,
            key="test_tag",
        )

        self.assertEqual(response.status_code, 200)

    def test_remove_tag_missing_key(self):
        mock_request = mock.MagicMock()
        mock_request.data = {}

        with self.assertRaises(TagNotFoundException):
            self.viewset.remove_tag(mock_request, pk=1)

    def test_bulk_remove_tags(self):
        mock_request = mock.MagicMock()
        mock_request.data = {"keys": ["tag1", "tag2"]}

        response = self.viewset.bulk_remove_tags(mock_request, pk=1)

        self.viewset.taggable_service.bulk_remove_tags.assert_called_once_with(
            instance=self.mock_object,
            keys=["tag1", "tag2"],
        )

        self.assertEqual(response.status_code, 200)

    def test_bulk_remove_tags_missing_keys(self):
        mock_request = mock.MagicMock()
        mock_request.data = {}

        with self.assertRaises(TagNotDefinedException):
            self.viewset.bulk_remove_tags(mock_request, pk=1)

    def test_bulk_remove_tags_with_many_instances(self):
        mock_request = mock.MagicMock()
        mock_request.data = {"objects": [1, 2], "keys": ["tag1", "tag2"]}

        response = self.viewset.bulk_remove_tags_with_many_instances(mock_request)

        self.mock_queryset.filter.assert_called_once_with(id__in=[1, 2])

        self.viewset.taggable_service.bulk_remove_tags_with_many_instances.assert_called_once_with(
            instances=self.mock_filtered_queryset,
            keys=["tag1", "tag2"],
        )

        self.assertEqual(response.status_code, 200)

    def test_bulk_remove_tags_with_many_instances_missing_keys(self):
        mock_request = mock.MagicMock()
        mock_request.data = {"objects": [1, 2]}

        with self.assertRaises(TagNotDefinedException):
            self.viewset.bulk_remove_tags_with_many_instances(mock_request)

    def test_bulk_remove_tags_with_many_instances_missing_objects(self):
        mock_request = mock.MagicMock()
        mock_request.data = {"keys": ["tag1", "tag2"]}

        with self.assertRaises(ObjectIDsNotDefinedException):
            self.viewset.bulk_remove_tags_with_many_instances(mock_request)

    def test_get_tags(self):
        mock_request = mock.MagicMock()

        tag_instance = {"tags": ["tag1", "tag2"]}
        self.viewset.taggable_service.get_tags.return_value = tag_instance

        response = self.viewset.get_tags(mock_request, pk=1)

        self.viewset.taggable_service.get_tags.assert_called_once_with(
            instance=self.mock_object,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, tag_instance)

    def test_get_tags_not_found(self):
        mock_request = mock.MagicMock()

        self.viewset.taggable_service.get_tags.return_value = None

        response = self.viewset.get_tags(mock_request, pk=1)

        self.assertEqual(self.viewset.taggable_service.get_tags.call_count, 1)

        self.assertEqual(response.status_code, 404)

    def test_filter_by_tag(self):
        mock_request = mock.MagicMock()
        mock_request.query_params = {"key": "test_tag"}
        mock_request.data = {}

        self.viewset.taggable_service.filter_by_tag.return_value = (
            self.mock_filtered_queryset
        )

        response = self.viewset.filter_by_tag(mock_request)

        self.viewset.taggable_service.filter_by_tag.assert_called_once_with(
            queryset=self.mock_queryset,
            key="test_tag",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"data": "serialized_data"})

    def test_filter_by_tag_missing_key(self):
        mock_request = mock.MagicMock()
        mock_request.query_params = {}
        mock_request.data = {}

        with self.assertRaises(TagNotDefinedException):
            self.viewset.filter_by_tag(mock_request)

    def test_filter_by_tag_with_pagination(self):
        mock_request = mock.MagicMock()
        mock_request.query_params = {"key": "test_tag"}
        mock_request.data = {}

        page = [self.mock_object]
        self.viewset.paginate_queryset.return_value = page

        paginated_response = Response({"results": {"data": "serialized_data"}})
        self.viewset.get_paginated_response = mock.MagicMock(
            return_value=paginated_response
        )

        self.viewset.taggable_service.filter_by_tag.return_value = (
            self.mock_filtered_queryset
        )

        response = self.viewset.filter_by_tag(mock_request)

        self.viewset.paginate_queryset.assert_called_once_with(
            self.mock_filtered_queryset
        )

        self.viewset.get_serializer.assert_called_once_with(page, many=True)

        self.viewset.get_paginated_response.assert_called_once_with(
            {"data": "serialized_data"}
        )

        self.assertEqual(response, paginated_response)

    def test_exclude_by_tag(self):
        mock_request = mock.MagicMock()
        mock_request.query_params = {"key": "test_tag"}
        mock_request.data = {}

        self.viewset.taggable_service.exclude_by_tag.return_value = (
            self.mock_filtered_queryset
        )

        response = self.viewset.exclude_by_tag(mock_request)

        self.viewset.taggable_service.exclude_by_tag.assert_called_once_with(
            queryset=self.mock_queryset,
            key="test_tag",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"data": "serialized_data"})

    def test_exclude_by_tag_missing_key(self):
        mock_request = mock.MagicMock()
        mock_request.query_params = {}
        mock_request.data = {}

        with self.assertRaises(TagNotDefinedException):
            self.viewset.exclude_by_tag(mock_request)

    def test_exclude_by_tag_with_pagination(self):
        mock_request = mock.MagicMock()
        mock_request.query_params = {"key": "test_tag"}
        mock_request.data = {}

        page = [self.mock_object]
        self.viewset.paginate_queryset.return_value = page

        paginated_response = Response({"results": {"data": "serialized_data"}})
        self.viewset.get_paginated_response = mock.MagicMock(
            return_value=paginated_response
        )

        self.viewset.taggable_service.exclude_by_tag.return_value = (
            self.mock_filtered_queryset
        )

        response = self.viewset.exclude_by_tag(mock_request)

        self.viewset.paginate_queryset.assert_called_once_with(
            self.mock_filtered_queryset
        )

        self.viewset.get_serializer.assert_called_once_with(page, many=True)

        self.viewset.get_paginated_response.assert_called_once_with(
            {"data": "serialized_data"}
        )

        self.assertEqual(response, paginated_response)
