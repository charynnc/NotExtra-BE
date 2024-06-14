"""
URL configuration for notebookBE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("sign_up/", views.sign_up, name='sign_up'),
    path("log_in/", views.log_in, name='log_in'),
    path("log_out/", views.log_out, name='log_out'),
    path("user_info/", views.user_info, name='user_info'),
    path("change_info/", views.change_info, name='change_info'),
    path("change_avatar/", views.change_avatar, name='change_avatar'),
    path("change_password/", views.change_password, name='change_password'),
    path("new_note/", views.new_note, name='new_note'),
    path("change_title/", views.change_title, name='change_title'),
    path("change_content/", views.change_content, name='change_content'),
    path("all_notes/", views.all_notes, name='all_notes'),
    path("get_notes_by_tag/", views.get_notes_by_tag, name='get_notes_by_tag'),
    path("delete_content/", views.delete_content, name='delete_content'),
    path("delete_note/", views.delete_note, name='delete_note'),
    path("classify_note/", views.classify_note, name='classify_note'),
    path("view_note/", views.view_note, name='view_note'),
    path("search_note/", views.search_note, name='search_note'),
    path("get_tags/", views.get_tags, name='get_tags'),
    path("get_user_tags/", views.get_user_tags, name='get_user_tags'),
    path("change_note_tag/", views.change_note_tag, name='change_note_tag'),
    path("change_user_tag/", views.change_user_tag, name='change_user_tag'),
    path("ai_text/", views.ai_text, name='ai_text'),
    path("init/", views.init, name='init'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
