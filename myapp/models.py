from django.db import models

# Create your models here.
host_name = 'http://10.0.2.2:8000/'


class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    avatar = models.CharField(
        max_length=100, default='media/default.png')
    user_id = models.CharField(default='0', max_length=5, primary_key=True)
    auth_id = models.CharField(max_length=20, default='')
    motto = models.CharField(max_length=100, default='My motto is ...')
    tags = models.JSONField(blank=True, null=True, default=list)


class Note(models.Model):
    title = models.CharField(max_length=100)
    user_id = models.CharField(default='0', max_length=5)
    note_id = models.CharField(default='0', max_length=5, primary_key=True)
    content_num = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    last_edit_time = models.DateTimeField(auto_now=True)
    tags = models.JSONField(blank=True, null=True, default=list)


class Content(models.Model):
    note_id = models.CharField(default='0', max_length=5)
    content_id = models.CharField(default='0', max_length=5, primary_key=True)
    order = models.IntegerField(default=0)
    type = models.CharField(max_length=20)
    detail = models.CharField(max_length=5000)


class Counter(models.Model):
    user_num = models.IntegerField(default=0)
    note_num = models.IntegerField(default=0)
    content_num = models.IntegerField(default=0)
