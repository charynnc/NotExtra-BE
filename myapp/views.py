from django.http import JsonResponse
from django.shortcuts import render
from .models import User, Counter
import json
import random
import string

# Create your views here.

# 生成包含大小写字母和数字的字符集合
characters = string.ascii_letters + string.digits
host_name = 'http://127.0.0.1:8000/'


def sign_up(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    # 查看用户名是否重复
    for user in User.objects.all():
        if user.username == username:
            return JsonResponse({"status": "refuse", "msg": "用户名已存在"})

    # 创建用户
    counter = Counter.objects.all()[0]
    User.objects.create(username=username, password=password,
                        avatar="", user_id=counter.UserNum+1)
    counter.UserNum += 1
    counter.save()

    return JsonResponse({"status": "success", "msg": "注册成功"})


def log_in(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    # 查看用户名是否存在
    for user in User.objects.all():
        if user.username == username:
            if user.password == password:
                # 随机生成auth_id
                random_string = ''.join(random.choice(characters)
                                        for _ in range(10))
                user.auth_id = random_string
                user.save()
                return JsonResponse({"status": "success", "msg": "登录成功", "username": user.username, "auth_id": random_string, "user_id": user.user_id, "motto": user.motto})
            else:
                return JsonResponse({"status": "refuse", "msg": "密码错误"})

    return JsonResponse({"status": "refuse", "msg": "用户名不存在"})


def log_out(request):
    user_id = request.POST.get("user_id")
    auth_id = request.POST.get("auth_id")
    for user in User.objects.all():
        if user.auth_id == auth_id and auth_id != '' and user.user_id == int(user_id):
            user.auth_id = ""
            user.save()
            return JsonResponse({"status": "success", "msg": "登出成功"})

    return JsonResponse({"status": "refuse", "msg": "用户未登录"})


def change_info(request):
    user_id = request.POST.get("user_id")
    auth_id = request.POST.get("auth_id")
    motto = request.POST.get("motto")
    username = request.POST.get("username")
    file = request.FILES
    avatar = file.get("avatar", None).read()

    for user in User.objects.all():
        if user.auth_id == auth_id and auth_id != '' and user.user_id == int(user_id):
            user.motto = motto
            user.username = username

            random_string = ''.join(random.choice(
                string.ascii_letters + string.digits) for _ in range(4))
            with open('media/user/'+user_id+'_'+random_string+'.jpg', 'wb') as f:
                f.write(avatar)
            user.avatar = host_name+'media/user/'+user_id+'_'+random_string+'.jpg'

            user.save()
            return JsonResponse({"status": "success", "msg": "修改成功"})

    return JsonResponse({"status": "refuse", "msg": "用户未登录"})


def init(request):
    Counter.objects.all().delete()
    Counter.objects.create(UserNum=0, NoteNum=0)
    return JsonResponse({"status": "success", "msg": "初始化成功"})
