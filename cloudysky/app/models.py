from django.db import models

class User(models.Model):
    class UserType(models.TextChoices):
        SERF = 'serf', 'Serf'
        ADMIN = 'admin', 'Admin'

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.SERF
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"username: {self.username}"

    def is_admin(self):
        return self.user_type == self.UserType.ADMIN

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"Profile for {self.user.username}"

class Media(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = 'image', 'Image'
        VIDEO = 'video', 'Video'
        AUDIO = 'audio', 'Audio'
        DOCUMENT = 'document', 'Document'
        OTHER = 'other', 'Other'

    url = models.URLField()
    media_type = models.CharField(max_length=20, choices=MediaType.choices, default=MediaType.OTHER)

    def __str__(self):
        return f"url: {self.url}, media_type: {self.media_type}"


class Post(models.Model):
    class SuppressionReason(models.TextChoices):
        OFFENSIVE = 'offensive', 'Offensive Content'
        SPAM = 'spam', 'Spam'
        MISINFORMATION = 'misinformation', 'Misinformation'
        HATE_SPEECH = 'hate_speech', 'Hate Speech'
        HARASSMENT = 'harassment', 'Harassment'
        PRIVACY = 'privacy', 'Privacy Violation'
        OTHER = 'other', 'Other'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_suppressed = models.BooleanField(default=False)
    reason_suppressed = models.CharField(
        max_length=20,
        choices=SuppressionReason.choices,
        blank=True
    )

    def __str__(self):
        return f"user: {self.user}, text: {self.text[:30]}"


class Comment(models.Model):
    class SuppressionReason(models.TextChoices):
        OFFENSIVE = 'offensive', 'Offensive Content'
        SPAM = 'spam', 'Spam'
        MISINFORMATION = 'misinformation', 'Misinformation'
        HATE_SPEECH = 'hate_speech', 'Hate Speech'
        HARASSMENT = 'harassment', 'Harassment'
        PRIVACY = 'privacy', 'Privacy Violation'
        OTHER = 'other', 'Other'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_suppressed = models.BooleanField(default=False)
    reason_suppressed = models.CharField(
        max_length=20,
        choices=SuppressionReason.choices,
        blank=True
    )

    def __str__(self):
        return f"user: {self.user}, post: {self.post}, text: {self.text[:30]}"


class PostMedia(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)

    def __str__(self):
        return f"post: {self.post}, media: {self.media}"


class CommentMedia(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)

    def __str__(self):
        return f"comment: {self.comment}, media: {self.media}"