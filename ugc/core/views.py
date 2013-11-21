# coding: utf-8
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.shortcuts import get_object_or_404
from ugc.core.models import Publish, Tag
from ugc.core.forms import ContactForm

# class HomepageView(TemplateView):
#     template_name = ''

class PublishDetailView(DetailView):
    model = Publish

def homepage(request):
    publishs = Publish.objects.all()
    context = { 'publishs' : publishs }
    return render(request, 'core/publish_list.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.enviar()
            form = ContactForm()
            sended = True
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form' : ContactForm()} )
