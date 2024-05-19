from django.db import models

# Create your models here.
host_name = 'http://10.0.2.2:8000/'


class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    avatar = models.CharField(
        max_length=100, default=host_name + 'media/default.png')
    user_id = models.CharField(default='0', max_length=5, primary_key=True)
    auth_id = models.CharField(max_length=20, default='')
    motto = models.CharField(max_length=100, default='My motto is ...')


class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.JSONField(blank=True, null=True, default=list)
    media = models.JSONField(blank=True, null=True, default=list)
    user_id = models.CharField(default='0', max_length=5, primary_key=True)
    note_id = models.CharField(default='0', max_length=5)
    create_time = models.DateTimeField(auto_now_add=True)
    last_edit_time = models.DateTimeField(auto_now=True)
    tags = models.JSONField(blank=True, null=True, default=list)


class Counter(models.Model):
    user_num = models.IntegerField(default=0)
    note_num = models.IntegerField(default=0)
