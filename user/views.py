from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from rest_framework.renderers import JSONRenderer
from user.models import *
from django.db.models import Q
from .forms import *
from baseUserCF import *

def login_in(func):#验证用户是否登录
    def a(request):
        a=request.session.get('login_in')
        if a:
            return func(request)
        else:
            return render(request,'user/login.html')
    return a
# Create your views here.
class JSONResponse(HttpResponse):
    def __init__(self,data,**kwargs):
        content=JSONRenderer().render(data)
        kwargs['content_type']='application/json'
        super(JSONResponse,self).__init__(content,**kwargs)
def index(request):
    user=User.objects.all()
    book=Book.objects.all()
    commen=Commen.objects.all()
    actions=Action.objects.all()
    liuyan=Liuyan.objects.all()
    num=Num.objects.get(id=1)
    num.users=len(user)
    num.books=len(book)
    num.commens=len(commen)
    num.actions=len(actions)
    num.liuyans=len(liuyan)
    num.save()
    return render(request,'user/index.html')
def login(request):
    if request.method == 'POST':
        form=Login(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            result=User.objects.filter(username=username)
            if result:
                user=User.objects.get(username=username)
                if user.password == password:
                    request.session['login_in']=True
                    request.session['user_id']=user.id
                    request.session['name']=user.name
                    return HttpResponseRedirect(reverse('allbook'))
                else:
                    return render(request,'user/login.html',{'form':form,'message':'密码错误'})
            else:
                return render(request,'user/login.html',{'form':form,'message':'账号不存在'})
    else:
        form=Login()
        return render(request,'user/login.html',{'form':form})
def register(request):
    if request.method =='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password2']
            email=form.cleaned_data['email']
            name=form.cleaned_data['name']
            phone=form.cleaned_data['phone']
            address=form.cleaned_data['address']
            a=User.objects.create(username=username,password=password,email=email,address=address,name=name,phone=phone)
            #根据表单数据创建一个新的用户
            return HttpResponseRedirect(reverse('login'))#跳转到登录界面
        else:
            return render(request,'user/register.html',{'form':form})#表单验证失败返回一个空表单到注册页面
    form=RegisterForm()
    return render(request,'user/register.html',{'form':form})
def logout(request):
    if not request.session.get('login_in',None):#不在登录状态跳转回首页
        return HttpResponseRedirect(reverse('index'))
    request.session.flush()#清除session信息
    return HttpResponseRedirect(reverse('index'))
def getRecom(name):
    import random
    # from os.path import exists  #增加缓存
    # if not exists('index/cache'):
    #     with open("index/cache",'w') as f:
    #         rates=Rate.objects.all()
    #         for i in rates:
    #             f.write(i.user.username+','+str(i.mark)+','+str(i.book.id)+'\n')
    #         print "cache ok"
    bookid_list =rec(name)
    recbook=[]
    #print bookid_list
    for item in bookid_list:
        b=Book.objects.get(id=item)
        recbook.append(b)
    if len(recbook)>6:
        recbook=random.sample(recbook,6)
    return recbook
@login_in
def item(request,id=None):

    book=getRecom(request.session.get('user_id'))
    return render(request,'user/item.html',locals())
def allbook(request):
    book=Book.objects.all()
    paginator=Paginator(book,9)
    page=request.GET.get('page',1)
    currentPage=int(page)
    book=paginator.page(page)
    return render(request,'user/allbook.html',{'book':book})
def search(request):#搜索
    if request.method == 'POST':#如果搜索界面
        key=request.POST['search']
        request.session['search']=key#记录搜索关键词解决跳页问题
    else:
        key=request.session.get('search')#得到关键词
    books=Book.objects.filter(Q(title__icontains=key)|Q(intro__icontains=key)|Q(author__icontains=key))#进行内容的模糊搜索
    if books:#如何商品存在
        paginator=Paginator(books,15)#分页，基本同上
        page_num=request.GET.get('page',1)
        try:
            book=paginator.page(page_num)
        except PageNotAnInteger:
            book=paginator.page(1)
        except EmptyPage:
            book=paginator.page(paginator.num_pages)
        return render(request,'user/search.html',{'book':book})
    else:
        return render(request,'user/search.html',{'message':'搜索无结'})
def book(request,book_id):
    try:
        user=User.objects.get(id=request.session.get('user_id'))
    except:
        pass
    try:
        collect=user.book_set.get(id=book_id)
    except:
        pass
    book=Book.objects.get(id=book_id)
    book.num+=1
    book.save()
    commen=book.commen_set.order_by('-addtime')
    return render(request,'user/book.html',locals())
def score(request,book_id):
    try:
        user=User.objects.get(id=request.session.get('user_id'))
    except:
        return HttpResponseRedirect(reverse('login'))
    book=Book.objects.get(id=book_id)
    Rate.objects.create(user=user,book=book,mark=float(request.POST.get('score')))
    try:
        score=book.score
    except:
        score=Score.objects.create(book=book)
    score.num +=1
    if score.num == 1:
        score.fen ='%.2f' % ((score.fen+float(request.POST.get('score')))/1)
    else:
        score.fen ='%.2f' % ((score.fen+float(request.POST.get('score')))/2)
    score.save()
    return HttpResponseRedirect(reverse('book',args=(book_id,)))
def commen(request,book_id):
    try:
        user=User.objects.get(id=request.session.get('user_id'))
    except:
        return HttpResponseRedirect(reverse('login'))
    book=Book.objects.get(id=book_id)
    try:
        score=book.score
    except:
        Score.objects.create(book=book)
    book.score.com +=1
    book.score.save()
    comment=request.POST.get('comment')
    Commen.objects.create(user=user,book=book,content=comment)
    return HttpResponseRedirect(reverse('book',args=(book_id,)))
def good(request,commen_id,book_id):
    commen=Commen.objects.get(id=commen_id)
    commen.good +=1
    commen.save()
    return HttpResponseRedirect(reverse('book',args=(book_id,)))
def collect(request,book_id):
    user=User.objects.get(id=request.session.get('user_id'))
    book=Book.objects.get(id=book_id)
    book.sump +=1
    book.collect.add(user)
    book.save()
    return HttpResponseRedirect(reverse('book',args=(book_id,)))
def decollect(request,book_id):
    user=User.objects.get(id=request.session.get('user_id'))
    book=Book.objects.get(id=book_id)
    book.sump -=1
    book.collect.remove(user)
    book.save()
    return HttpResponseRedirect(reverse('book',args=(book_id,)))
def liuyan(request):
    liuyan=Liuyan.objects.all()
    return render(request,'user/liuyan.html',{'liuyan':liuyan})
def newliuyan(request):
    user=User.objects.get(id=request.session.get('user_id'))
    title=request.POST.get('title')
    content=request.POST.get('content')
    Liuyan.objects.create(user=user,content=content,title=title)
    return HttpResponseRedirect(reverse('liuyan'))
def liuyanson(request,liuyan_id):
    liuyan=Liuyan.objects.get(id=liuyan_id)
    son=liuyan.liuyanson_set.all()
    return render(request,'user/sonliuyan.html',{'i':liuyan,'son':son})
def soncommen(request,liuyan_id):
    liuyan=Liuyan.objects.get(id=liuyan_id)
    liuyan.num +=1
    liuyan.save()
    user=User.objects.get(id=request.session.get('user_id'))
    content=request.POST.get('content')
    print(content)
    Liuyanson.objects.create(user=user,content=content,liuyan=liuyan)
    return HttpResponseRedirect(reverse('liuyanson',args=(liuyan_id,)))
@login_in
def personal(request):
    user=User.objects.get(id=request.session.get('user_id'))
    if request.method =='POST':
        form=Edit(instance=user,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('personal'))
        else:
            return render(request,'user/personal.html',{'message':'修改失败','form':form})
    form=Edit(instance=user)
    return render(request,'user/personal.html',{'form':form})
@login_in
def mycollect(request):
    user=User.objects.get(id=request.session.get('user_id'))
    book=user.book_set.all()
    return render(request,'user/mycollect.html',{'book':book})
@login_in
def myjoin(request):
    user=User.objects.get(id=request.session.get('user_id'))
    action=user.action_set.all()
    return render(request,'user/myaction.html',{'action':action})
@login_in
def mycommen(request):
    user=User.objects.get(id=request.session.get('user_id'))
    commen=user.commen_set.all()
    return render(request,'user/mycommen.html',{'commen':commen})
@login_in
def delcom(request,commen_id):
    commen=Commen.objects.get(id=commen_id)
    commen.book.score.com -=1
    commen.book.score.save()
    commen.delete()
    return HttpResponseRedirect(reverse('mycommen'))
@login_in
def myrate(request):
    user=User.objects.get(id=request.session.get('user_id'))
    rate=user.rate_set.all()
    return render(request,'user/myrate.html',{'rate':rate})
def delrate(request,rate_id):
    rate=Rate.objects.get(id=rate_id)
    rate.delete()
    return HttpResponseRedirect(reverse('myrate'))
def maxbook(request):
    book=Book.objects.order_by('sump')
    book=book[0:10]
    return render(request,'user/maxbook.html',{'book':book})
def newbook(request):
    book=Book.objects.order_by('-id')
    book=book[0:10]
    return render(request,'user/newbook.html',{'book':book})
def nbbook(request):
    books=Book.objects.all()
    book=[]
    for i in books:
        if i.good=='诺贝尔文学奖':
            book.append(i)
    return render(request,'user/nbbook.html',{'book':book})
def mdbook(request):
    books=Book.objects.all()
    book=[]
    for i in books:
        if i.good=='茅盾文学奖':
            book.append(i)
    return render(request,'user/mdbook.html',{'book':book})
def begin(request):
    if request.method=='POST':
        email=request.POST['email']
        username=request.POST['username']
        result=User.objects.filter(username=username)
        if result:
            if result[0].email==email:
                result[0].password=request.POST['password']
                return HttpResponse("修改密码成功")
            else:
                return render(request,'user/begin.html',{'message':'注册时的邮箱不对'})
        else:
            return render(request,'user/begin.html',{'message':'账号不存在'})
    return render(request,'user/begin.html')
def kindof(request):
    tags=Tags.objects.all()
    return render(request,'user/kindof.html',{'tags':tags})
def kind(request,kind_id):
    tags=Tags.objects.get(id=kind_id)
    book=tags.tags.all()
    return render(request,'user/kind.html',{'book':book})
def recom(name):
    import random
    # from os.path import exists  #增加缓存
    # if not exists('index/cache'):
    #     with open("index/cache",'w') as f:
    #         rates=Rate.objects.all()
    #         for i in rates:
    #             f.write(i.user.username+','+str(i.mark)+','+str(i.book.id)+'\n')
    #         print "cache ok"
    bookid_list = adjustrecommend(name)
    recbook=[]
    #print bookid_list
    for item in bookid_list:
        b=Book.objects.get(id=item)
        recbook.append(b)
    if len(recbook)>6:
        recbook=random.sample(recbook,6)
    return recbook
def zhouitem(request,id=None):
    try:
        book=recom(request.session.get('user_id'))
    except Exception as e:
        book=None
        #print e
    return render(request,'user/item.html',locals())
