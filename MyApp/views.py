from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from MyApp.models import *

# Create your views here.
# 欢迎页面
@login_required
def welcome(request):
    return render(request,'welcome.html')

# 项目列表
@login_required
def project_list(request):
    return render(request,'welcome.html',{'whichHTML':'project_list.html','oid':''})

# 接口库
def interface(request):
    return render(request,'interface.html')

# 帮助页面
@login_required
def api_help(request):
    return render(request,'welcome.html',{'whichHTML':'help.html','oid':''})

# 不同页面返回不同数据：数据分发器
def child_json(eid,oid=''):
    if eid == 'home.html':
        date = DB_home_href.objects.all()
        res = {"hrefs":date}
        return res
    if eid == 'project_list.html':
        date = DB_project.objects.all()
        res = {"projects":date}
        return res
    if eid == 'P_apis.html':
        project = DB_project.objects.filter(id=oid)[0]
        res = {'project':project}
        return res
    if eid == 'P_cases.html':
        project = DB_project.objects.filter(id=oid)[0]
        res = {'project':project}
        return res
    if eid == 'P_project_set.html':
        project = DB_project.objects.filter(id=oid)[0]
        res = {'project':project}
        return res

# 返回子页面
def child(request,eid,oid):
    res = child_json(eid,oid)
    return render(request,eid,res)

# 主页
@login_required
def home(request):
    return render(request,'welcome.html',{'whichHTML' : 'home.html',"oid":""})

# 登录页面
def login(request):
    return render(request,'login.html')

# 登录
def login_action(request):
    u_name = request.GET['username']
    p_word = request.GET['password']
    user = auth.authenticate(username = u_name,password = p_word)
    if user is not None:
        auth.login(request,user)
        request.session['user'] = u_name
        return HttpResponse('登录成功')
    else:
        return HttpResponse('登录失败')

# 用户注册
def register_action(request):
    u_name = request.GET['username']
    p_word = request.GET['password']
    try:
        user = User.objects.create_user(username=u_name,password=p_word)
        user.save()
        return HttpResponse('注册成功')
    except:
        return HttpResponse('用户名已存在，注册失败！')

# 用户退出
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')

# 吐槽
def pei(request):
    tucao_text = request.GET['tucao_text']
    DB_tucao.objects.create(user=request.user.username,text=tucao_text)
    return HttpResponse('成功')

# 删除项目
def delete_project(request):
    id = request.GET['id']
    DB_project.objects.filter(id=id).delete()
    return HttpResponse('删除成功')

# 新增项目
def add_project(request):
    project_name = request.GET['project_name']
    project_otheruser = request.GET['project_otheruser']
    project_remark = request.GET['project_remark']
    DB_project.objects.create(name=project_name,remark=project_remark,other_user=project_otheruser,user=request.user.username)
    return HttpResponse('新增成功')

# 接口库
@login_required
def open_apis(request,id):
    project_id = id
    return render(request,'welcome.html',{'whichHTML' : 'P_apis.html',"oid":project_id})

# 用例设计
@login_required
def cases(request,id):
    project_id = id
    return render(request,'welcome.html',{'whichHTML' : 'P_cases.html',"oid":project_id})

# 项目设置
@login_required
def project_set(request,id):
    project_id = id
    return render(request,'welcome.html',{'whichHTML' : 'P_project_set.html',"oid":project_id})

# 保存项目设置
def save_project_set(request,id):
    project_id = id
    name = request.GET['name']
    remark = request.GET['remark']
    other_user = request.GET['other_user']
    DB_project.objects.filter(id=project_id).update(name=name,remark=remark,other_user=other_user)
    return HttpResponse('保存成功')


