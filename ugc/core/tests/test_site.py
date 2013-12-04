# coding: utf-8
from django.test import TestCase
from django.core.urlresolvers import reverse as r
from ugc.core.forms import ContactForm
from ugc.core.models import Publish, User

class HomepageTest(TestCase):
    def setUp(self):
        u = User.objects.create(name='Thiago', email='email@email.com')
        Publish.objects.create(title='Noticia', description='Descricao', user=u)
        self.resp = self.client.get(r('core:homepage'))

    def test_get(self):
        'GET / must return status code 200.'
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        'Homepage must use template index.html'
        self.assertTemplateUsed(self.resp, 'core/publish_list.html')

    def test_html(self):
        'Html must contain input controls'
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 2)
        self.assertContains(self.resp, '<button', 1)
        self.assertContains(self.resp, 'type="text"', 1)
        self.assertContains(self.resp, 'type="submit"', 1)

    def test_context(self):
        'Publish must be in context'
        total = len(self.resp.context['publishs'])
        self.assertEqual(1, total)

class DetailTest(TestCase):
    def setUp(self):
        u = User.objects.create(name='Thiago', email='email@email.com')
        publish = Publish(title='Noticia teste', description='Descricao da noticia', user=u)
        publish.save()
        self.resp = self.client.get(r('core:detail', args=[publish.id]))

    def test_get(self):
        'GET /publicacao/1/ shoud return status code 200.'
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        'Response shoud be a rendered template'
        self.assertTemplateUsed(self.resp, 'core/publish_detail.html')

    def test_context(self):
        'Publish must be in context'
        publish = self.resp.context['publish']
        self.assertIsInstance(publish, Publish)

class AboutTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('core:about'))

    def test_get(self):
        'GET /sobre/ must return status code 200.'
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        'About must use template about.html'
        self.assertTemplateUsed(self.resp, 'about.html')

class ContactTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('core:contact'))

    def test_get(self):
        'GET /contato/ return status code 200'
        self.assertEqual(200, self.resp.status_code)

    def test_csrf(self):
        'Html must contain csrf token'
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_template(self):
        'Contact must use template contact.html'
        self.assertTemplateUsed(self.resp, 'contact.html')

    def test_has_form(self):
        'Context must have the contact form'
        form = self.resp.context['form']
        self.assertIsInstance(form, ContactForm)

    def test_form_has_fields(self):
        'Form must have 3 fiels'
        form = self.resp.context['form']
        self.assertItemsEqual(['name','email','message'], form.fields)

    def test_html(self):
        'Html must contain input controls'
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 4)
        self.assertContains(self.resp, '<textarea', 1)
        self.assertContains(self.resp, '<button', 2)
        self.assertContains(self.resp, 'type="text"', 2)
        self.assertContains(self.resp, 'type="submit"', 2)

class ContactPostTest(TestCase):
    def setUp(self):
        data = dict(name='Thiago Dorneles',
                    email='thiagodorneles@me.com',
                    message='mensagem de teste')
        self.resp = self.client.post(r('core:contact'), data)

    def test_post(self):
        'Valid POST should redirect to /contato/'
        self.assertEqual(200, self.resp.status_code)

    def test_context(self):
        s = self.resp.context['sended']
        self.assertEqual(s, True)