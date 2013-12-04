# coding: utf-8
from django.test import TestCase
from django.core.urlresolvers import reverse as r
from ugc.core.models import Publish, Tag, User

class SearchTest(TestCase):
    def setUp(self):
        u = User.objects.create(name='Thiago', email='email@email.com')
        Publish.objects.create(title='alagamento em cachoeirinha', description='alagamento em cachoeirinha', user=u)
        data = dict(search='cacho')
        self.resp = self.client.post(r('core:search'), data)
        # self.resp = self.client.get(r('core:search', args=['alagamento']))

    def test_get(self):
        'GET /search must return status code 200.'
        self.assertEqual(200, self.resp.status_code)

    def test_results(self):
        'Result of search'
        self.assertEqual(1, len(self.resp.context['publishs']))


class TagSearchTest(TestCase):
    def setUp(self):
        t1 = Tag.objects.create(tag='acidente')
        u = User.objects.create(name='Thiago', email='email@email.com')
        p1 = Publish.objects.create(title='alagamento em cachoeirinha', description='descricao', user=u)
        p2 = Publish.objects.create(title='acidente', description='Descricao', user=u)
        p1.tags.add(t1)
        p2.tags.add(t1)
        self.resp = self.client.get(r('core:search_tags', args=['acidente']))

    def test_get(self):
        'GET /tags/ must return status code 200.'
        self.assertEqual(200, self.resp.status_code)

    def test_context(self):
        'Publishs must be in context with search tags.'
        self.assertEqual(2, len(self.resp.context['publishs']))

