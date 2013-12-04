# coding: utf-8
from django.test import TestCase
from datetime import datetime
from django.db import IntegrityError
from ugc.core.models import Publish, Tag, User

class PublishTest(TestCase):
    def setUp(self):
        u = User.objects.create(name='Thiago', email='email@email.com')
        self.publish = Publish(title='Noticia teste', 
                               description='Descricao da noticia',
                               user=u)

    def test_create(self):
        'Publish must have title and description'
        self.publish.save()
        self.assertEqual(1, self.publish.pk)

    def test_has_created_at(self):
        'Publish must have automatic created_at'
        self.publish.save()
        self.assertIsInstance(self.publish.created_at, datetime)

    def test_unicode(self):
        'Publish must return a title with unicode'
        self.assertEqual(u'Noticia teste', unicode(self.publish))

    def test_tags(self):
        'Publish has many Tags and vice-versa'
        self.publish.save()
        self.publish.tags.create(tag='esporte')
        self.assertEqual(1, self.publish.tags.count())

    def test_multiple_tags(self):
        'Publish has many Tags and vice-versa'
        self.publish.save()
        self.publish.tags.create(tag='esporte')
        self.publish.tags.create(tag='acidente')
        self.assertEqual(2, self.publish.tags.count())

class PublishUniqueTest(TestCase):
    def setUp(self):
        u = User.objects.create(name='Thiago', email='email@email.com')
        Publish.objects.create(title='Noticia teste', 
                               description='Descricao da noticia',
                               user=u)

    def test_unique(self):
        'Title and description together must be unique'
        publish = Publish(title='Noticia teste', description='Descricao da noticia')
        self.assertRaises(IntegrityError, publish.save)

class TagTest(TestCase):
    def setUp(self):
        self.tag = Tag(tag='esporte')

    def test_create(self):
        'Tag must have tag field'
        self.tag.save()
        self.assertEqual(1, self.tag.pk)

    def test_has_created_at(self):
        'Tag mush have automatic created_at'
        self.tag.save()
        self.assertIsInstance(self.tag.created_at, datetime)

    def test_unicode(self):
        'Tag must return a Tag at unicode'
        self.assertEqual(u'esporte', unicode(self.tag))

class TagUniqueTest(TestCase):
    def setUp(self):
        Tag.objects.create(tag='esporte')

    def test_unique_tag(self):
        'Tag must have unique'
        tag = Tag(tag='esporte')
        self.assertRaises(IntegrityError, tag.save)
