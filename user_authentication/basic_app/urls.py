#from django.conf.urls import include, url
from django.urls import path
from . import views

app_name = 'basic_app'

urlpatterns =[
    path(r'register/', views.register, name='register'),
    path(r'login/', views.user_login, name='login'),
    #url(r'^help/', views.help, name='help'),
]
