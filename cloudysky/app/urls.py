from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index.html', views.index, name='index'),
    path('app/new', views.new_user_form, name='new_user_form'),
    path('app/createUser', views.create_user, name='create_user'),
]