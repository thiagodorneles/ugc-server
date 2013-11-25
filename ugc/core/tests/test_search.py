# coding: utf-8
from django.test import TestCase
from django.core.urlresolvers import reverse as r
from ugc.core.models import Publish, Tag

class SearchTest(TestCase):
    def setUp(self):
        Publish.objects.create(title='alagamento em cachoeirinha', description='alagamento em cachoeirinha')
        self.resp = self.client.get(r('core:search', args=['alagamento']))

    def test_get(self):
        'GET /search must return status code 200.'
        self.assertEqual(200, self.resp.status_code)

    def test_results(self):
        'Result of search'
        self.assertEqual(1, len(self.resp.context['publishs']))


class TagSearchTest(TestCase):
    def setUp(self):
        t1 = Tag.objects.create(tag='acidente')
        p1 = Publish.objects.create(title='alagamento em cachoeirinha', description='descricao')
        p2 = Publish.objects.create(title='acidente', description='Descricao')
        p1.tags.add(t1)
        p2.tags.add(t1)
        self.resp = self.client.get(r('core:search_tags', args=['acidente']))

    def test_get(self):
        'GET /tags/ must return status code 200.'
        self.assertEqual(200, self.resp.status_code)

    def test_context(self):
        'Publishs must be in context with search tags.'
        self.assertEqual(2, len(self.resp.context['publishs']))

