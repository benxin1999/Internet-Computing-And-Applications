from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register',views.signup),
    path('login',views.login),
    path('modify/password',views.modify_password),
    path('modify/userInfo',views.modify_userInfo),
    path('get/userInfo',views.get_userinfo)


]