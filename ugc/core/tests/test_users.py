# coding: utf-8
from django.test import TestCase
from datetime import datetime
from django.db import IntegrityError
from ugc.core.models import User

class UserTest(TestCase):
    def setUp(self):
        self.user = User(name='Thiago', email='email@email.com')

    def test_create(self):
        'User must have a name and email'
        self.user.save()
        self.assertEqual(1, self.user.id)

    def test_has_created_at(self):
        'User must have automatic created_at'
        self.user.save()
        self.assertIsInstance(self.user.created_at, datetime)

    def test_unicode(self):
        'User must return a name with unicode'
        self.assertEqual('Thiago', unicode(self.user))

class UserUniqueTest(TestCase):
    def setUp(self):
        User.objects.create(name='Thiago', email='email@email.com')

    def test_unique(self):
        'User must have unique by name'
        u = User(name='Thiago', email='email@email.com')
        self.assertIsInstance(IntegrityError, u.save)

