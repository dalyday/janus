from django.shortcuts import render,HttpResponse,redirect
from crm.form import LoginFrom
from django.conf import settings #此处的setting包含了自定义+内置
# from day12 import settings      #此处的setting仅包含用户自定义
from crm.utils.md5 import md5
from crm import models
from rbac.service import permission
from django.contrib.sessions.backends.db import SessionStore


""" 两个验证，第一个是form验证，第二个是帐号或者密码不存在错误 """
def login(request):
    if request.method == "GET":
        form = LoginFrom()
        return render(request, 'login.html', {'form': form})
    else:
        form = LoginFrom(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)  通过form验证可以拿到前端的用户名，密码 {'username': '代海风', 'password': '123'}
            form.cleaned_data['password'] = md5(form.cleaned_data['password'])
            user = models.UserInfo.objects.filter(**form.cleaned_data).first()
            #另外两种
            # models.UserInfo.objects.filter(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            # models.UserInfo.objects.filter(**{'username':'daly','password':123456})
            if user:
                # 将用户信息放置到session中,user是个对象，python只能序列化字典，元组
                # 获取当前用户的所有角色
                # role_liat = user.roles.all()
                # print(role_liat)   打印出来的为对象，使用__str__回调函数可以显示中文
                permission.init_permission(user, request)  # 跟init_permission函数关联，作用权限初始化
                return redirect('/index/')
            else:
                form.add_error('password', '用户名或密码错误')
        return render(request, 'login.html', {'form': form})

def reset_permission(request):
    """
    权限重置
    :param request:
    :return:
    """
    # 找到人 如：name = 'bob'
    # 获取这个人的session_key
    # 在session表中将该用户的数据删除
    # obj = models.UserInfo.objects.filter(name=name).first()
    # permission.reset_permission(obj.session_key,request)
    if request.method == 'GET':
        user_list = models.UserInfo.objects.all()
        return render(request,'reset_permission.html',{'user_list':user_list})
    else:
        username = request.POST.get('username')
        obj = models.UserInfo.objects.filter(username=username).first()
        # print(username,obj.session_key)
        if obj.session_key:
            permission.reset_permission(obj.session_key,request)
        return redirect('/reset/permission/')



def index(request):
    """
    部门管路
    :return:
    """
    return render(request,'index.html')

def custom1(request):
    """
    部门管路
    :return:
    """
    return render(request,'custom1.html')

def custom2(request):
    """
    部门管路
    :return:
    """
    return render(request,'custom2.html')

def custom3(request):
    """
    部门管路
    :return:
    """
    return render(request,'custom3.html')

def custom4(request):
    """
    部门管路
    :return:
    """
    return render(request,'custom4.html')