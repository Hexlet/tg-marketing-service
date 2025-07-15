from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import View


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            'index.html'
        )