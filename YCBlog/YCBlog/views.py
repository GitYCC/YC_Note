from django.shortcuts import render,redirect,render_to_response

from django.http import cookie
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import Http404
from Posts.models import Post
from Accounts.models import Account
from django.middleware.csrf import get_token

import pprint, re, datetime, logging, os
from YCBlog import settings

from django.core.cache import cache

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def record_ip(request):
    ip = get_client_ip(request)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    method = request.method
    path = request.get_full_path()
    agent = request.META.get('HTTP_USER_AGENT')
    user = request.user
    ID_list = cache.get('record_ip_ID')
    html_ID = os.path.join(settings.BASE_DIR,"log_ID.html")
    html_log = os.path.join(settings.BASE_DIR,"log.html")
    if not ID_list:
        if not os.path.isfile(html_ID): open(html_ID,'a').close()
        with open(html_ID,"r") as f: 
            ID_list = []
            for line in f.readlines():
                index, custom = line.strip().split('|||')
                ID_list.append(custom)
            cache.set("record_ip_ID",ID_list,3000)
    custom = "{}|{}".format(ip,agent)
    if custom not in ID_list:
        with open(html_ID,"a") as f:
            f.write('ID{:05d}'.format(len(ID_list))+"|||"+custom+"\n")
        ID_list.append(custom)
        cache.set("record_ip_ID",ID_list,3000)

    ID = ID_list.index(custom)
    string = "{}|ID{:05d}|{} {}|:|\n".format(now,ID,method,path)
    with open(html_log,"a") as f:
        f.write(string)

def log(request):
    if not verify_cookie(request): return redirect('/god/login/')
    output = ''
    with open(os.path.join(settings.BASE_DIR,"log_ID.html"),"r") as f:
        readlines = "".join(f.readlines())
        readlines = readlines.replace("\n","<br/>")
        output += readlines
    output += '--------------<br/>'
    with open(os.path.join(settings.BASE_DIR,"log.html"),"r") as f:
        readlines = "".join(f.readlines())
        readlines = readlines.replace("\n","<br/>")
        output += readlines
    return HttpResponse(output)



def welcome(request):
    record_ip(request)
    if request.method == 'GET':
        return render(request,'welcome.html',{})


    elif request.method == 'POST':
        pass


def me(request):

    record_ip(request)
    if request.method == 'GET':
        me_post = Post.objects.filter(kind__contains="Me").filter(isPublic__exact=True)[0]
        return render(request,'me.html',{'post':me_post})


    elif request.method == 'POST':
        pass


    


def coding(request):
    record_ip(request)

    if request.method == 'GET':
        posts = cache.get('coding_posts')
        if not posts:
            logging.warning("recharge cache with 'coding'")
            posts = Post.objects.filter(kind__contains="Coding").filter(isPublic__exact=True)
            posts = posts.order_by('-post_time')
            cache.set("coding_posts",posts,1800)
           

        return render(request,'posts.html',
            {'posts':posts,'title':"Coding",
            'subtitle':"Mechine Learning | Algorithm | Python",
            'front_board_img':"https://dl.dropboxusercontent.com/s/21l1n4gii0t50bj/coding_front_board.jpg"
            })


    elif request.method == 'POST':
        pass

def reading(request):
    record_ip(request)
    if request.method == 'GET':
        posts = cache.get('reading_posts')
        if not posts:
            logging.warning("recharge cache with 'reading'")
            posts = Post.objects.filter(kind__contains="Reading").filter(isPublic__exact=True)
            posts = posts.order_by('-post_time')
            cache.set("reading_posts",posts,1800)

        return render(request,'posts.html',
            {'posts':posts,'title':"Reading",
            'subtitle':"Be a Scientist",
            'front_board_img':"https://dl.dropboxusercontent.com/s/6g1hdd1e3vak32o/reading_front_board.jpg"
            })


    elif request.method == 'POST':
        pass

def living(request):
    record_ip(request)
    if request.method == 'GET':
        posts = cache.get('living_posts')
        if not posts:
            logging.warning("recharge cache with 'living'")
            posts = Post.objects.filter(kind__contains="Living").filter(isPublic__exact=True)
            posts = posts.order_by('-post_time')
            cache.get("living_posts",posts,1800)

        return render(request,'posts.html',
            {'posts':posts,'title':"Living",
            'subtitle':"My Life is Brilliant",
            'front_board_img':"https://dl.dropboxusercontent.com/s/98tsgzu2pv2j65h/living_front_board.jpg"
            })


    elif request.method == 'POST':
        pass

def post(request,pk):
    record_ip(request)
    if request.method == 'GET':
        post = Post.objects.get(pk=pk)

        if not post.front_board:
            if post.kind == "Coding":
                post.front_board = "https://dl.dropboxusercontent.com/s/21l1n4gii0t50bj/coding_front_board.jpg"
            elif post.kind == "Reading":
                post.front_board = "https://dl.dropboxusercontent.com/s/6g1hdd1e3vak32o/reading_front_board.jpg"
            elif post.kind == "Living":
                post.front_board = "https://dl.dropboxusercontent.com/s/98tsgzu2pv2j65h/living_front_board.jpg"

        if not post:
            return Http404
        else:
            return render(request,'post.html',
                {'post':post})


    elif request.method == 'POST':
        pass



def set_cookie(response, key, value, days_expire = 0.5):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  #one year
    else:
        max_age = days_expire * 24 * 60 * 60 
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires,httponly=True)
    return response


def login(request):
    record_ip(request)
    if request.method == 'GET':
        return render(request,'login.html',{})
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            account = Account.objects.filter(username__exact=username)[0]
            if account: 
                h = account.hash_password
                if Account.valid_password(username,password,h):
                    username_cookie = Account.hashUsername(account.username)
                    response = redirect('/god/admin/')
                    return set_cookie(response,'si-um-zr', username_cookie)
                

        return render(request,'login.html',{'err':"wrong user or password"})

def logout(request):
    record_ip(request)
    if request.method == 'GET':
        response = redirect('/god/login/')
        return set_cookie(response,'si-um-zr', "")


def verify_cookie(request):
    if 'si-um-zr' in request.COOKIES:
        username = Account.checkHashUsername(request.COOKIES['si-um-zr'])
        if username: return True
    return False


def myadmin(request):
    record_ip(request)
    if not verify_cookie(request): return redirect('/god/login/')
    if request.method == 'GET':
        username = Account.checkHashUsername(request.COOKIES['si-um-zr'])
        posts = Post.objects.all()
        return render(request,'admin.html',{"username":username,"posts":posts})
        

def post_edit(request,pk):
    record_ip(request)
    if not verify_cookie(request): return redirect('/god/login/')
    if request.method == 'GET':      
        if not pk=="000":
            post = Post.objects.get(pk=pk)
            post.post_time = post.post_time.strftime("%Y-%m-%d %H:%M")
            return render(request,'post_edit.html',{"post":post,"isNew":"False"})
        else:
            post = {}
            post["post_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            return render(request,'post_edit.html',{"post":post,"isNew":"True"})

        
    elif request.method == 'POST':
        isNew = True if request.POST.get("isNew")=="True" else False
        aDict = {key:request.POST.get(key) for key in ['title','content','file','kind','tags','author','front_board','post_time']}
        aDict['isPublic'] = True if 'isPublic' in request.POST else False

        if isNew:
            if  aDict['title'] and aDict['kind'] and aDict['author'] and aDict['post_time']:
                Post.objects.create(**aDict)
                return redirect('/god/admin/')
            else:
                return render(request,'post_edit.html',{"post":aDict,"isNew":"True"})
        else:
            if  aDict['title'] and aDict['kind'] and aDict['author'] and aDict['post_time']:
                post = Post.objects.get(pk=pk)
                post.save_by_dict(aDict)
                return redirect('/god/admin/')
            else:
                return render(request,'post_edit.html',{"post":aDict,"isNew":"False"})
            
            return render(request,'post_edit.html',{"post":post})

def post_delete(request,pk):
    #request = get_token(request)
    if not verify_cookie(request): return redirect('/god/login/')
    if request.method == 'POST':
        if pk == "000":
            return redirect('/god/admin/')
        post = Post.objects.get(pk=pk)
        post.delete()    
        return redirect('/god/admin/')

def post_preview(request,pk):
    if not verify_cookie(request): return redirect('/god/login/')
    if request.method == 'GET':   
        return post(request,pk)


def flush_cache(request):
    if not verify_cookie(request): return redirect('/god/login/')
    cache._cache.flush_all()
    return redirect('/god/admin/')


    