from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed_view, name='index'),
    path('index.html', views.feed_view, name='index'),
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

    # New API endpoints for CloudySky
    path('app/feed', views.api_feed, name='api_feed'),
    path('app/post/<int:post_id>', views.api_post_detail, name='api_post_detail'),
    path('app/user/profile/<int:user_id>', views.user_profile, name='user_profile'),
    path('app/user/profile/edit', views.edit_user_profile, name='edit_user_profile'),
    path('app/admin/dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('app/admin/user/stats', views.user_stats, name='user_stats'),

    # View routes
    path('app/moderation', views.moderation_view, name='moderation'),
    path('app/post_view/<int:post_id>', views.post_view, name='post_view'),
]