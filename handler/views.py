from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

class Index(TemplateView):
    def get(self, *args, **kwargs):
        return render(self.request , 'handler/index.html')

