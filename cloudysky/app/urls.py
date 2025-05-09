from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index.html', views.index, name='index'),
    path('app/new', views.new_user_form, name='new_user_form'),
    path('app/createUser', views.create_user, name='create_user'),
    # New API endpoints and views for HW5
    path('app/new_post', views.new_post, name='new_post'),
    path('app/new_comment', views.new_comment, name='new_comment'),
    path('app/createPost', views.create_post, name='create_post'),
    path('app/createComment', views.create_comment, name='create_comment'),
    path('app/hidePost', views.hide_post, name='hide_post'),
    path('app/hideComment', views.hide_comment, name='hide_comment'),
    path('app/dumpFeed', views.dump_feed, name='dump_feed'),
]