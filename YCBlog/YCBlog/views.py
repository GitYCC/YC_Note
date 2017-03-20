from django.shortcuts import render

from django.http import cookie
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import Http404
from Posts.models import Post

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
        posts = Post.objects.filter(kind__contains="Coding").filter(isPublic__exact=True)
        posts = posts.order_by('-post_time')
        return render(request,'posts.html',
            {'posts':posts,'title':"Coding",
            'subtitle':"Mechine Learning X Algorithm X Python",
            'front_board_img':"/static/welcome/front_board_img.jpg"
            })


    elif request.method == 'POST':
        pass

def reading(request):

    if request.method == 'GET':
        posts = Post.objects.filter(kind__contains="Reading").filter(isPublic__exact=True)
        posts = posts.order_by('-post_time')
        return render(request,'posts.html',
            {'posts':posts,'title':"Reading",
            'subtitle':"Be a Scientist",
            'front_board_img':"/static/welcome/front_board_img.jpg"
            })


    elif request.method == 'POST':
        pass

def living(request):

    if request.method == 'GET':
        posts = Post.objects.filter(kind__contains="Living").filter(isPublic__exact=True)
        posts = posts.order_by('-post_time')
        return render(request,'posts.html',
            {'posts':posts,'title':"Living",
            'subtitle':"My Life is Brilliant",
            'front_board_img':"/static/welcome/front_board_img.jpg"
            })


    elif request.method == 'POST':
        pass

def post(request,pk):

    if request.method == 'GET':
        post = Post.objects.get(pk=pk)
        if not post:
            return Http404
        else:
            return render(request,'post.html',
                {'post':post})


    elif request.method == 'POST':
        pass


