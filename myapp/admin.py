from django.contrib import admin
from .models import User, Note, Counter, Content
# Register your models here.

admin.site.register(User)
admin.site.register(Note)
admin.site.register(Counter)
admin.site.register(Content)
