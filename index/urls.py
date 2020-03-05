# coding: utf-8
from django.urls import path
from .views import *

app_name = 'index'

urlpatterns = [
    path('index/', index, name='index'),
    path('login/', login, name='login'),
    path('get_code/', get_code, name='get_code'),
    path('test_captcha/', test_captcha, name='test_captcha'),
    path('save/', save, name='save'),
    path('query/', query, name='query'),
    path('update/', update, name='update'),
    path('delete_data/', delete_data, name='delete_data'),
]
