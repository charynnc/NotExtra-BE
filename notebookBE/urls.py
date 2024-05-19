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
    path("new_content/", views.new_content, name='new_content'),
    path("init/", views.init, name='init'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
