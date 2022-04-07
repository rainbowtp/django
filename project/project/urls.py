"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,re_path,include

from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('<int:id>/index/', views.id_index, name='id_index'),
    path('<int:id>/info/', views.id_info, name='id_info'),
    path('<int:id>/add/', views.id_add, name='id_add'),
    path('<int:id>/secret/', views.id_secret, name='id_secret'),
    path('<int:id>/<int:data_id>/delete/', views.id_delete, name='id_delete'),
    path('<int:id>/<int:data_id>/edit/', views.id_edit, name='id_edit'),

    path('show/', views.show, name='show'),

    # path('insert', views.register, name='insert'),



    # path("index/",views.index),
    # path("timer/",views.timer),

    # # 分组
    # re_path(r'^articles/([0-9]{4})/$', views.year_article, name='y_a'),
    # re_path(r'^articles/([0-9]{4})/([0-9]{2})/$', views.month_archive),
    # # re_path(r'^articles/([0-9]{4})/([0-9]{2})/([0-9]+)/$', views.article_detail),
    
    # # 命名空间
    # re_path(r'^articles/(?P<y>[0-9]{4})/(?P<m>[0-9]{2})/$', views.month_archive),

    # path('login/', views.login, name='Login'),

    # # 反向解析
    # re_path(r'^articles/20033/$', views.articles, name='a'),


    ]

