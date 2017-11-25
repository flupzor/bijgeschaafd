
from django.test import TestCase, override_settings

from ..es import ESObjectList
from ..models import Version
from .factory_models import VersionFactory


class ESObjectListTests(TestCase):
    def test_es_object_list(self):
        v1, v2, v3, v4, v5 = VersionFactory.create_batch(5)
        example_request = {
            "from": 100,
            "size": 10,
            "query": {
                "match_phrase": {"body": 'test'},
            },
            "sort": [
                {"date": "desc"},
            ]
        }
        example_results = {
            'hits': {
                'total': 500,
                'hits': [
                    { '_id': v1.pk, '_source': {}},
                    { '_id': v2.pk, '_source': {}},
                    { '_id': v3.pk, '_source': {}},
                    { '_id': v4.pk, '_source': {}},
                    { '_id': v5.pk, '_source': {}},
                ]
            }
        }

        object_list = ESObjectList(example_request, example_results, Version)

        self.assertEquals(object_list.count(), 500)
        self.assertEquals(len(object_list), 500)
        self.assertEquals(
            set(object_list[100:105].values_list('pk', flat=True)),
            set([v1.pk, v2.pk, v3.pk, v4.pk,v5.pk]))
