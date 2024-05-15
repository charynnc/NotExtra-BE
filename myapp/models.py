from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    avatar = models.CharField(max_length=100)
    user_id = models.IntegerField(default=0, primary_key=True)
    auth_id = models.CharField(max_length=20, default='')
    motto = models.CharField(max_length=100, default='')


class Counter(models.Model):
    UserNum = models.IntegerField(default=0)
    NoteNum = models.IntegerField(default=0)
