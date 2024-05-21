import base64
import os
from django.http import JsonResponse
from django.shortcuts import render
from .models import User, Counter, Note, Content
from django.views.decorators.csrf import csrf_exempt
import json
import random
import string

# Create your views here.

# 生成包含大小写字母和数字的字符集合
characters = string.ascii_letters + string.digits
host_name = 'http://10.0.2.2:8000/'


@csrf_exempt
def sign_up(request):
    print(request.POST)
    username = request.POST.get("username")
    password = request.POST.get("password")
    # 查看用户名是否重复
    for user in User.objects.all():
        if user.username == username:
            return JsonResponse({"status": "refuse", "msg": "用户名已存在"})

    # 创建用户
    counter = Counter.objects.all()[0]
    User.objects.create(username=username, password=password,
                        user_id=str(counter.user_num+1))
    counter.user_num += 1
    counter.save()

    return JsonResponse({"status": "success", "msg": "注册成功"})


@csrf_exempt
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


@csrf_exempt
def log_out(request):
    user_id = request.POST.get("user_id")
    auth_id = request.POST.get("auth_id")
    user = User.objects.filter(user_id=user_id)
    if user:
        user = user[0]
        if user.auth_id != auth_id:
            return JsonResponse({"status": "refuse", "msg": "用户未登录"})
        user.auth_id = ""
        user.save()

    return JsonResponse({"status": "refuse", "msg": "用户未登录"})


@csrf_exempt
def change_avatar(request):
    print(request.POST)
    user_id = request.POST.get("user_id")
    auth_id = request.POST.get("auth_id")

    file = request.FILES
    avatar = file.get("avatar", None).read()
    # avatar_base64 = request.POST.get("avatar")
    # try:
    #     avatar_data = base64.b64decode(avatar_base64)
    # except Exception as e:
    #     print(e)
    #     return JsonResponse({'status': 'error', 'message': 'Invalid base64 string.'})

    user = User.objects.filter(user_id=user_id)
    if user:
        user = user[0]
        if user.auth_id != auth_id:
            return JsonResponse({"status": "refuse", "msg": "用户未登录"})

        random_string = ''.join(random.choice(
            string.ascii_letters + string.digits) for _ in range(4))
        with open('media/user/'+user_id+'_'+random_string+'.jpg', 'wb') as f:
            f.write(avatar)
        user.avatar = host_name+'media/user/'+user_id+'_'+random_string+'.jpg'
        user.save()

    return JsonResponse({"status": "success", "msg": "修改成功"})


@csrf_exempt
def change_info(request):
    print(request.POST)
    user_id = request.POST.get("user_id")
    auth_id = request.POST.get("auth_id")
    motto = request.POST.get("motto")
    username = request.POST.get("username")

    user = User.objects.filter(username=username)
    if user:
        return JsonResponse({"status": "refuse", "msg": "该用户名已被占用"})

    user = User.objects.filter(user_id=user_id)
    if user:
        user = user[0]
        if user.auth_id != auth_id:
            return JsonResponse({"status": "refuse", "msg": "用户未登录"})
        else:
            user.motto = motto
            user.username = username
            user.save()
            return JsonResponse({"status": "success", "msg": "修改成功"})
    else:
        return JsonResponse({"status": "refuse", "msg": "用户不存在"})


@csrf_exempt
def change_password(request):
    print(request.POST)
    user_id = request.POST.get("user_id")
    auth_id = request.POST.get("auth_id")
    old_password = request.POST.get("old_password")
    new_password = request.POST.get("new_password")

    user = User.objects.filter(user_id=user_id)
    if user:
        user = user[0]
        if user.auth_id != auth_id:
            return JsonResponse({"status": "refuse", "msg": "用户未登录"})
        else:
            if user.password == old_password:
                user.password = new_password
                user.save()
                return JsonResponse({"status": "success", "msg": "修改成功"})
            else:
                return JsonResponse({"status": "refuse", "msg": "原密码错误"})
    else:
        return JsonResponse({"status": "refuse", "msg": "用户不存在"})


def user_info(request):
    print(request.GET)
    user_id = request.GET.get("user_id")
    auth_id = request.GET.get("auth_id")

    user = User.objects.filter(user_id=user_id)
    if user:
        user = user[0]
        if user.auth_id != auth_id:
            return JsonResponse({"status": "refuse", "msg": "用户未登录"})
        else:
            data = {"status": "success", "msg": "查询成功",
                    "username": user.username, "avatar": user.avatar, "motto": user.motto}
            print(data)
            return JsonResponse(data)
    else:
        return JsonResponse({"status": "refuse", "msg": "用户不存在"})


@csrf_exempt
def new_note(request):
    print(request.POST)
    user_id = request.POST.get("user_id")
    auth_id = request.POST.get("auth_id")
    title = request.POST.get("title")

    user = User.objects.filter(user_id=user_id)
    if user:
        user = user[0]
        if user.auth_id != auth_id:
            return JsonResponse({"status": "refuse", "msg": "用户未登录"})
        else:
            counter = Counter.objects.all()[0]
            note_id = str(counter.note_num + 1)
            counter.note_num += 1
            counter.save()
            Note.objects.create(title=title, user_id=user_id,
                                note_id=note_id)
            return JsonResponse({"status": "success", "msg": "创建成功"})
    else:
        return JsonResponse({"status": "refuse", "msg": "用户不存在"})


@csrf_exempt
def change_content(request):
    print(request.POST)
    user_id = request.POST.get("user_id")
    auth_id = request.POST.get("auth_id")
    note_id = request.POST.get("note_id")
    type = request.POST.get("type")
    order = request.POST.get("order")
    operation = request.POST.get("operation")

    user = User.objects.filter(user_id=user_id)
    if user:
        user = user[0]
        if user.auth_id != auth_id:
            return JsonResponse({"status": "refuse", "msg": "用户未登录"})
        else:
            # 生成content
            if type == "text":
                content = request.POST.get("content")
            else:
                # 如果是文件，保存后记录url
                file = request.FILES.get("content", None)
                random_string = ''.join(random.choice(
                    string.ascii_letters + string.digits) for _ in range(4))
                ext = os.path.splitext(file.name)[1]
                path = 'media/note/'+note_id+'_'+random_string+ext
                with open(path, 'wb') as f:
                    f.write(file.read())
                content = host_name+path

            note = Note.objects.filter(note_id=note_id)
            if note:
                note = note[0]
                note.content_num += 1
                counter = Counter.objects.all()[0]
                content_id = str(counter.content_num + 1)
                counter.content_num += 1
                counter.save()

                if operation == "add":
                    # 更新已有content的order
                    if int(order) <= note.content_num:
                        contents = Content.objects.filter(
                            note_id=note_id, order__gte=int(order))
                        for content in contents:
                            content.order += 1
                            content.save()

                    Content.objects.create(note_id=note_id, content_id=content_id, order=int(order),
                                        type=type, content=content)
                elif operation == "edit":
                    content = Content.objects.filter(note_id=note_id, order=int(order))
                    if content:
                        content = content[0]
                        content.content = content
                        content.save()
                    else:
                        return JsonResponse({"status": "refuse", "msg": "内容不存在"})
                note.save()

            return JsonResponse({"status": "success", "msg": "创建成功"})
    else:
        return JsonResponse({"status": "refuse", "msg": "用户不存在"})


def all_notes(request):
    print(request.GET)
    user_id = request.GET.get("user_id")
    auth_id = request.GET.get("auth_id")

    user = User.objects.filter(user_id=user_id)
    if user:
        user = user[0]
        if user.auth_id != auth_id:
            return JsonResponse({"status": "refuse", "msg": "用户未登录"})
        else:
            notes = Note.objects.filter(user_id=user_id)
            data = []
            for note in notes:
                # 生成摘要
                contents = Content.objects.filter(note_id=note.note_id)
                if contents:
                    content = contents[0]
                    if content.type == "text":
                        abstract = content.content[:20]
                    elif content.type == "image":
                        abstract = "[图片]"
                    elif content.type == "audio":
                        abstract = "[音频]"
                    elif content.type == "video":
                        abstract = "[视频]"
                    else:
                        abstract = ""

                data.append({"note_id": note.note_id, "title": note.title,
                             "create_time": note.create_time.strftime("%Y-%m-%d %H:%M:%S"), "last_edit_time": note.last_edit_time.strftime("%Y-%m-%d %H:%M:%S"), "abstract": abstract, "tags": note.tags})
            return JsonResponse({"status": "success", "msg": "查询成功", "data": data})
    else:
        return JsonResponse({"status": "refuse", "msg": "用户不存在"})

@csrf_exempt
def delete_content(request):
    print(request.POST)
    user_id = request.POST.get("user_id")
    auth_id = request.POST.get("auth_id")
    note_id = request.POST.get("note_id")
    content_id = request.POST.get("content_id")

    user = User.objects.filter(user_id=user_id)
    if user:
        user = user[0]
        if user.auth_id != auth_id:
            return JsonResponse({"status": "refuse", "msg": "用户未登录"})
        else:
            content = Content.objects.filter(note_id=note_id, content_id=content_id)
            if content:
                content = content[0]
                content.delete()
                # 更新order
                contents = Content.objects.filter(note_id=note_id, order__gt=content.order)
                for content in contents:
                    content.order -= 1
                    content.save()
                return JsonResponse({"status": "success", "msg": "删除成功"})
            else:
                return JsonResponse({"status": "refuse", "msg": "内容不存在"})
    else:
        return JsonResponse({"status": "refuse", "msg": "用户不存在"})

@csrf_exempt
def delete_note(request):
    print(request.POST)
    user_id = request.POST.get("user_id")
    auth_id = request.POST.get("auth_id")
    note_id = request.POST.get("note_id")

    user = User.objects.filter(user_id=user_id)
    if user:
        user = user[0]
        if user.auth_id != auth_id:
            return JsonResponse({"status": "refuse", "msg": "用户未登录"})
        else:
            note = Note.objects.filter(note_id=note_id)
            if note:
                note = note[0]
                note.delete()
                contents = Content.objects.filter(note_id=note_id)
                for content in contents:
                    content.delete()
                return JsonResponse({"status": "success", "msg": "删除成功"})
            else:
                return JsonResponse({"status": "refuse", "msg": "笔记不存在"})
    else:
        return JsonResponse({"status": "refuse", "msg": "用户不存在"})

@csrf_exempt
def change_tag(request):
    print(request.POST)
    user_id = request.POST.get("user_id")
    auth_id = request.POST.get("auth_id")
    note_id = request.POST.get("note_id")
    tag = request.POST.get("tag")
    operation = request.POST.get("operation")

    user = User.objects.filter(user_id=user_id)
    if user:
        user = user[0]
        if user.auth_id != auth_id:
            return JsonResponse({"status": "refuse", "msg": "用户未登录"})
        else:
            note = Note.objects.filter(note_id=note_id)
            if note:
                note = note[0]
                tags = note.tags
                if operation == "add":
                    tags.append(tag)
                elif operation == "delete":
                    tags.remove(tag)

                note.tags = tags
                note.save()
                return JsonResponse({"status": "success", "msg": "修改成功"})
            else:
                return JsonResponse({"status": "refuse", "msg": "笔记不存在"})
    else:
        return JsonResponse({"status": "refuse", "msg": "用户不存在"})

def classify_note(request):
    print(request.GET)
    user_id = request.GET.get("user_id")
    auth_id = request.GET.get("auth_id")
    tag = request.GET.get("tag")

    user = User.objects.filter(user_id=user_id)
    if user:
        user = user[0]
        if user.auth_id != auth_id:
            return JsonResponse({"status": "refuse", "msg": "用户未登录"})
        else:
            notes = Note.objects.filter(user_id=user_id, tags__contains=[tag])
            data = []
            for note in notes:
                # 生成摘要
                contents = Content.objects.filter(note_id=note.note_id)
                if contents:
                    content = contents[0]
                    if content.type == "text":
                        abstract = content.content[:20]
                    elif content.type == "image":
                        abstract = "[图片]"
                    elif content.type == "audio":
                        abstract = "[音频]"
                    elif content.type == "video":
                        abstract = "[视频]"
                    else:
                        abstract = ""

                data.append({"note_id": note.note_id, "title": note.title,
                             "create_time": note.create_time.strftime("%Y-%m-%d %H:%M:%S"), "last_edit_time": note.last_edit_time.strftime("%Y-%m-%d %H:%M:%S"), "abstract": abstract, "tags": note.tags})
            return JsonResponse({"status": "success", "msg": "查询成功", "data": data})
    else:
        return JsonResponse({"status": "refuse", "msg": "用户不存在"})

def view_note(request):
    print(request.GET)
    user_id = request.GET.get("user_id")
    auth_id = request.GET.get("auth_id")
    note_id = request.GET.get("note_id")

    user = User.objects.filter(user_id=user_id)
    if user:
        user = user[0]
        if user.auth_id != auth_id:
            return JsonResponse({"status": "refuse", "msg": "用户未登录"})
        else:
            note = Note.objects.filter(note_id=note_id)
            if note:
                note = note[0]
                contents = Content.objects.filter(note_id=note_id)
                data = []
                for content in contents:
                    data.append({"content_id": content.content_id, "order": content.order,
                                 "type": content.type, "content": content.content})
                return JsonResponse({"status": "success", "msg": "查询成功", "title": note.title, "create_time": note.create_time.strftime("%Y-%m-%d %H:%M:%S"), "last_edit_time": note.last_edit_time.strftime("%Y-%m-%d %H:%M:%S"), "tags": note.tags, "contents": data})
            else:
                return JsonResponse({"status": "refuse", "msg": "笔记不存在"})
    else:
        return JsonResponse({"status": "refuse", "msg": "用户不存在"})


def init(request):
    for user in User.objects.all():
        user.avatar = host_name + 'media/default.png'
        user.motto = 'My motto is ...'
        user.save()
    return JsonResponse({"status": "success", "msg": "初始化成功"})
