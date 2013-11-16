# coding: utf-8
from django.shortcuts import render
from ugc.core.forms import ContactForm
from django.http import HttpResponseRedirect

def homepage(request):
    return render(request, 'index.html')

def detail(request, pk):
    return render(request, 'detail.html')    

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
