from django.shortcuts import render

# Create your views here.
# from django.shortcuts import render


from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from mysite import models


# from mysite import models


# user_list = [
#     {'user': 'jack', 'pwd': 'abc'},
#     {'user': 'tom', 'pwd': 'efcg'},
# ]

class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密 码', widget=forms.PasswordInput())


def regist(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            # 获取表单数据
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            # 添加到数据库
            # User.objects.get_or_create(username = username,password = password)
            same_name_user = models.UserInfo.objects.filter(username=username)
            if same_name_user:  # 用户名唯一
                message = '用户已经存在，请重新选择用户名！'

                return render(req, 'share.html', {'registAdd': message, 'username': username})
            else:
                registAdd = models.UserInfo.objects.get_or_create(username=username, password=password)
                message = '注册成功'
                return render(req, 'share.html', {'registAdd': message})

    else:
        uf = UserForm()
    return render(req, 'regist.html', {'uf': uf}, )


def login(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            # 对比提交的数据与数据库中的数据
            user = models.UserInfo.objects.filter(username__exact=username, password__exact=password)
            if user:
                # 比较成功，跳转index
                response = HttpResponseRedirect('/index/')
                # 将username写入浏览器cookie，失效时间为3600
                response.set_cookie('username', username, 3600)
                return response
            else:
                return HttpResponseRedirect('/login/')
    else:
        uf = UserForm()
    return render(req, 'login.html', {'uf': uf}, )


# 登录成功
def index(req):
    username = req.COOKIES.get('username', '')
    return render(req, 'index.html', {'username': username})


# 退出登录

def logout(req):
    response = HttpResponse('logout!!!')
    # 清除cookie里保存的username
    response.delete_cookie('username')
    return response


def share(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']

            return render(req, 'share.html', {'username': username})
    else:
        uf = UserForm()
    return render(req, 'share.html', {'uf': uf})
# def index(request):
#     if request.method == 'POST':
#         username = request.POST.get('username', None)
#         password = request.POST.get('password', None)
#         models.UserInfo.objects.create(user=username, pwd=password)
#
#     user_list = models.UserInfo.objects.all()
#     return render(request, 'index.html', {'data': user_list})
