# coding: utf-8
from django.shortcuts import render
# from django.views.generic import TemplateView, DetailView, FormView, ListView
from django.shortcuts import get_object_or_404
from ugc.core.models import Publish, Tag
from ugc.core.forms import ContactForm, PublishSeachForm
from django.db.models import Q

# class HomepageView(TemplateView):
#     template_name = ''

def detail(request, pk):
    publish = Publish.objects.get(pk=pk)
    publish.update_views()
    return render(request, 'core/publish_detail.html', { 'publish' : publish })

# class PublishDetailView(DetailView):
#     model = Publish

def list(request, publishs, search=None):
    context = { 'publishs' : publishs, 'form': PublishSeachForm(), 'search': search }
    return render(request, 'core/publish_list.html', context)

def homepage(request):
    publishs = Publish.objects.all()
    return list(request, publishs)

def about(request):
    return render(request, 'about.html')

def contact(request):
    sended = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.enviar()
            form = ContactForm()
            sended = True
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form' : ContactForm(), 'sended' : sended } )

def search(request):
    slug = request.POST.get('search')
    publishs = Publish.objects.filter(Q(title__icontains=slug) | 
                                      Q(description__icontains=slug) |
                                      Q(city__icontains=slug) |
                                      Q(tags__tag__icontains=slug))

    return list(request, publishs, slug)

def search_tags(request, slug):
    publishs = Publish.objects.filter(tags__tag=slug)
    return list(request, publishs)