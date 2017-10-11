from django.shortcuts import render,redirect,render_to_response

from django.http import cookie
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import Http404
from Posts.models import Post
from Accounts.models import Account
from django.middleware.csrf import get_token

import pprint, re, datetime, logging, os, math
from YCBlog import settings

from django.core.cache import cache

def get_setting():
    SETTING = cache.get('SETTING')
    if not SETTING:
        SETTING = eval('{'+str(Post.objects.filter(kind__contains="Setting")[0].content.replace('\n',''))+'}')
        cache.set("SETTING",SETTING,1800)
    #pprint.pprint(SETTING)
    return SETTING

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


def robots(request):
    if request.method == 'GET':  
        return render(request,"robots.txt")
    elif request.method == 'POST':
        pass

def sitemap(request):

    if request.method == 'GET':

        tags = cache.get('all_tags')
        posts = cache.get('all_posts')
        if not tags or not posts:
            logging.warning("recharge cache with 'sitemap'")
            posts = Post.objects.exclude(kind__contains="Me").filter(isPublic__exact=True)
            posts = posts.order_by('-post_time')

            tags = get_tags(posts)

            cache.set("all_posts",posts,1800)
            cache.set("all_tags",tags,1800)

        newest_post = posts[0]
        
        return render(request,'sitemap.xml',
            {'posts':posts,
             'tags':tags,
             'newest_post':newest_post
            })
     

    elif request.method == 'POST':
        pass


def welcome(request):
    record_ip(request)
    if request.method == 'GET':
        

        recent_posts = cache.get('recent_posts')
        all_tag = cache.get('all_tag')
        if not recent_posts or not all_tag:
            max_files = 15
            logging.warning("recharge cache with 'recent'")
            posts = Post.objects.exclude(kind__contains="Me").filter(isPublic__exact=True)
            posts = posts.order_by('-post_time')

            recent_posts = posts[0:min(max_files,len(posts))]
            all_tag = get_tags(posts)

            cache.set("recent_posts",recent_posts,1800)
            cache.set("all_tag",all_tag,1800)
        
        SETTING = get_setting()
        return render(request,'welcome.html',{'KINDS':[(kind,SETTING['Kind'][kind]['page_title']) for kind in SETTING['Kind_List']],
                                              'recent_posts':recent_posts,
                                              'all_tag':all_tag,
                                              'TITLE': SETTING['Index']['page_TITLE'],
                                              'DESCRIPTION':"{} | {} | {}".format(SETTING['Index']['page_DESCRIPTION'],
                                                        ", ".join([tag for tag in all_tag]),
                                                        get_posts_title_list(recent_posts)),
                                              'title':SETTING['Index']['page_title'],
                                              'subtitle':SETTING['Index']['page_subtitle'],
                                              'pic':SETTING['Index']['page_pic'],

                                              })


    elif request.method == 'POST':
        pass

def redirect_welcome(request):
    return redirect('/')






def me(request):

    record_ip(request)

    if request.method == 'GET':
        SETTING = get_setting()
        me_post = Post.objects.filter(kind__contains=SETTING['Me']['name']).filter(isPublic__exact=True)[0]
        return render(request,'me.html',{'KINDS':[(kind,SETTING['Kind'][kind]['page_title'])for kind in SETTING['Kind_List']],
                                        'post':me_post,
                                        'TITLE':SETTING['Me']['page_TITLE'],
                                        'DESCRIPTION':SETTING['Me']['page_DESCRIPTION'],
                                        'title':SETTING['Me']['page_title'],
                                        'subtitle':SETTING['Me']['page_subtitle'],
                                        'pic':SETTING['Me']['page_pic'],
                                        })


    elif request.method == 'POST':
        pass

def get_tags(posts):
    tags = []
    for post in posts:
        for tag in post.tags.split(','):
            if tag!='' and tag not in tags: tags.insert(0,tag)
    return tags

def get_posts_from_tag(tag):
    name = 'tag_{}'.format(str(tag.encode('utf8')).replace(' ','\s')[2:-1])

    posts = cache.get(name)
    if not posts:
        logging.warning("recharge cache with '{}'".format(name))
        posts = Post.objects.filter(tags__contains=tag).filter(isPublic__exact=True)
        posts = posts.order_by('title').all()  
        posts = list(filter(lambda x: tag in x.tags.split(","),posts))
        cache.set(name,posts,1800)

    return posts

def get_page_info(posts,page,main):
    page_info = {}
    if not page: 
        page = 1
    else:
        page = int(page)
        
    if page < 1: raise Http404

    PAGE_MAX_POSTS = 5
    max_page = max([1,math.ceil(len(posts)*1.0/PAGE_MAX_POSTS)])
    if page > max_page: raise Http404


    all_page = []
    i = 0
    j = page - 2
    while(i<5 and j<=max_page):
        if j <= 0:
            j += 1
        else:
            all_page.append(j)
            i += 1 
            j += 1

    posts = posts[(page-1)*PAGE_MAX_POSTS : min([page*PAGE_MAX_POSTS,len(posts)])]


    page_info['now_page'] = page
    page_info['max_page'] = max_page
    page_info['all_page'] = all_page
    page_info['main'] = main 

    return posts, page_info

def get_posts_title_list(posts):
    return ", ".join([post.title for post in posts])


def render_kind(request,page=None,kind=None):
    record_ip(request)

    kind_title = kind.title()
    kind_low = kind.lower()
    
    SETTING = get_setting()

    if kind_title not in SETTING['Kind'].keys(): raise Http404

    if request.method == 'GET':
        cache_name = '{}_posts'.format(kind_low)
        posts = cache.get(cache_name)
        if not posts:
            logging.warning("recharge cache with '{}'".format(kind_low))
            posts = Post.objects.filter(kind__contains=SETTING['Kind'][kind_title]['name']).filter(isPublic__exact=True)
            posts = posts.order_by('-post_time')
            cache.set(cache_name,posts,1800)
        

        show_posts, page_info = get_page_info(posts=posts,page=page,main='/{}/'.format(kind_low))


        return render(request,'posts.html',
            {'KINDS':[(kind,SETTING['Kind'][kind]['page_title'])for kind in SETTING['Kind_List']],
            'posts':show_posts,
            'title':SETTING['Kind'][kind_title]['page_title'],
            'subtitle':SETTING['Kind'][kind_title]['page_subtitle'],
            'front_board_img':SETTING['Kind'][kind_title]['page_pic'],
            'TITLE':SETTING['Kind'][kind_title]['page_TITLE'],
            'DESCRIPTION':"{} | {}".format(SETTING['Kind'][kind_title]['page_DESCRIPTION'],get_posts_title_list(show_posts)),
            'tags':get_tags(posts),
            'page_info':page_info,

            })


    elif request.method == 'POST':
        pass

def tag(request,tag,page=None):
    record_ip(request)
    if request.method == 'GET':

        posts = get_posts_from_tag(tag)

        if len(posts)==0: raise Http404
        
        show_posts, page_info = get_page_info(posts=posts,page=page,main='/tag__{}/'.format(tag))

        SETTING = get_setting()
        return render(request,'posts.html',
            {'KINDS':[(kind,SETTING['Kind'][kind]['page_title'])for kind in SETTING['Kind_List']],
            'posts':show_posts,
            'title':"Tag",
            'subtitle':tag,
            'front_board_img':"https://dl.dropboxusercontent.com/s/x8d5iqpf76xy4xv/watercolor-580689_1280.jpg",
            'TITLE':"Tag: {}".format(tag),
            'DESCRIPTION':"{} | {}".format(tag,get_posts_title_list(show_posts)),
            'page_info':page_info,
            })


    elif request.method == 'POST':
        pass

def get_post_description(post_content):
    string_list = post_content.split('</p>')

    string_list = string_list[min(0,len(string_list)):min(5,len(string_list))]

    value = '</p>'.join(string_list)+'</p>'

    value = re.sub(r'\n[\n\s]+',' ',value, flags=re.MULTILINE)
    value = value.replace("\t"," ").replace('"','').strip()
    value = re.sub(r'<\s*img[^\n]+/\s*>','',value, flags=re.MULTILINE)
    value = re.sub(r'<[^>\n]+>','',value, flags=re.MULTILINE)

    
    return value

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


        if post.tags:
            posts_tag = {tag: get_posts_from_tag(tag) for tag in post.tags.split(',')}
        else:
            posts_tag = None


        if not post: raise Http404

        
        SETTING = get_setting()
        return render(request,'post.html',
                {'KINDS':[(kind,SETTING['Kind'][kind]['page_title'])for kind in SETTING['Kind_List']],
                'post':post, 
                 'TITLE':"{}".format(str(post.title)),
                 'DESCRIPTION':str(get_post_description(post.content)),
                 'posts_tag':posts_tag,

                 })


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
    SETTING = get_setting()
    if request.method == 'GET':
        return render(request,'login.html',{'KINDS':[(kind,SETTING['Kind'][kind]['page_title'])for kind in SETTING['Kind_List']],})
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
                

        return render(request,'login.html',
            {'KINDS':[(kind,SETTING['Kind'][kind]['page_title'])for kind in SETTING['Kind_List']],
            'err':"wrong user or password"})

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


        return render(request,'admin.html',
            {
            'TITLE': 'Admin',
            "username":username,"posts":posts})
        

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

def google_console(request):
    return render(request,"googleb03eb416eb102f2d.html")

    