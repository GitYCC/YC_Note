from django.shortcuts import render

from django.http import cookie
from django.http import HttpRequest
from django.http import HttpResponse

import pprint
# Create your views here.

def welcome(request):
    #l = filter(lambda x: x.startswith('HTTP_'),request.META.keys())
    #l = list(l)
    #print(l)
    #for i in l:
    #    print("{}, {}".format(i,str(request.META[i])))

    if request.method == 'GET':
        return render(request,'welcome.html',{})


    elif request.method == 'POST':
        pass


def me(request):
    #l = filter(lambda x: x.startswith('HTTP_'),request.META.keys())
    #l = list(l)
    #print(l)
    #for i in l:
    #    print("{}, {}".format(i,str(request.META[i])))

    if request.method == 'GET':
        return render(request,'me.html',{})


    elif request.method == 'POST':
        pass

def coding(request):

    if request.method == 'GET':
        return render(request,'coding.html',{})


    elif request.method == 'POST':
        pass

def reading(request):

    if request.method == 'GET':
        return render(request,'reading.html',{})


    elif request.method == 'POST':
        pass

def living(request):

    if request.method == 'GET':
        return render(request,'living.html',{})


    elif request.method == 'POST':
        pass