from elasticsearch import Elasticsearch, helpers


class ESObjectList(object):
    """
    Very simple wrapper around elastic search and django models
    which creates a object list of django orm objects, which
    have been found using elastic search.

    This object list can then be used as input for the django paginator.
    """
    def __init__(self, query, results, model):
        self.query = query
        self.results = results
        self.model = model

    @classmethod
    def search(cls, index, query, model):
        """
        :param index str elastic search index.
        :param query dict elastic search query, following query dsl.
        :param results dict results as returned by elasticsearch.Elasticsearch
        :param model The django ORM class which should be used to find the results
                     in the database.
        """
        client = Elasticsearch()
        results = client.search(index=index, body=query)
        return cls(query, results, model)

    def count(self):
        return self.results['hits']['total']

    def __len__(self):
        return self.count()

    def __getitem__(self, index):
        _from = self.query['from']
        if isinstance(index, slice):
            assert index.start >= _from
            assert index.stop >= _from
            assert index.stop <= _from + self.query['size']

            _start = index.start - _from
            _stop = index.stop - _from
            _step = index.step

            pks = [result['_id'] for result in self.results['hits']['hits'][_start:_stop:_step]]
            return self.model.objects.filter(pk__in=pks)

        index_in_result = index - _from
        pk = self.results['hits']['hits'][index_in_result]['_id']
        return self.model.objects.get(pk=pk)
