# from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse


def mainpage(request):
    template = 'home.html'
    # return HttpResponse('Hello!')
    return render(request, template)


def aboutpage(request):
    template = 'about.html'
    # return HttpResponse('Description!')
    return render(request, template)