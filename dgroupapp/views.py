from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DeleteView
from django.urls import reverse_lazy


class IndexView(TemplateView):
    template_name = 'index.html'
# Create your views here.
