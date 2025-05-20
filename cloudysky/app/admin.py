from django.contrib import admin
from .models import User, UserProfile, Media, Post, Comment, PostMedia, CommentMedia

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'created_at')
    list_filter = ('user_type', 'created_at')
    search_fields = ('username', 'email')
    inlines = [UserProfileInline]

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'is_suppressed', 'reason_suppressed')
    list_filter = ('is_suppressed', 'created_at', 'reason_suppressed')
    search_fields = ('title', 'text', 'user__username')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'created_at', 'is_suppressed', 'reason_suppressed')
    list_filter = ('is_suppressed', 'created_at', 'reason_suppressed')
    search_fields = ('text', 'user__username', 'post__title')

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('url', 'media_type')
    list_filter = ('media_type',)

admin.site.register(PostMedia)
admin.site.register(CommentMedia)
