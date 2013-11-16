# coding: utf-8
from django import forms
from django.core.mail import send_mail

class ContactForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=100)
    message = forms.Field(widget=forms.Textarea)

    def enviar(self):
        subject = 'site'
        to = 'thiagodornelesrs@gmail.com'
        message = """
         Nome: %(name)s
         E-mail: %(email)s
         Mensagem: %(message)s """ % self.cleaned_data

        send_mail(  subject=subject, message=message, from_email=self.cleaned_data.get('email'), recipient_list=[to] )


