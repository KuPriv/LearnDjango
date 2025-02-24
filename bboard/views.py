from django.shortcuts import render

from .models import Bb


def index(request):
    bbs = Bb.objects.order_by('-published')
    context = {'bbs': bbs, 'title': 'Объявления'}
    return render(request, 'bboard/index.html', context)