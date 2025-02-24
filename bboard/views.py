from django.shortcuts import render

from .models import Bb


def index(request):
    bbs = Bb.objects.all()
    context = {'bbs': bbs, 'title': 'Объявления'}
    return render(request, 'bboard/index.html', context)
