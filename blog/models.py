from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.core.validators import MinValueValidator

# Create your models here.

User = get_user_model()


class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class MoviePost(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    author = models.ForeignKey(User, related_name="posts", null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, related_name="posts", on_delete=models.SET_NULL, null=True, blank=True)
    movie_name = models.CharField(max_length=100)
    synopsis = models.TextField(blank=True)
    my_review = models.TextField(blank=True)
    year = models.IntegerField(validators=[MinValueValidator(1900),], default=1900)
    duration = models.CharField(max_length=10, default="00h00")
    image = models.ImageField(upload_to='post/image/%Y/%m', blank=True, null=True)
    gif = models.ImageField(upload_to='post/gif/%Y/%m', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author} {self.movie_name}"

    class Meta:
        ordering = ["-created_at"]


class Reaction(models.Model):
    class Type(models.TextChoices):
        LAUGHT = "😂", "😂" 
        SAD = "😥", "😥"
        NICE = "🔥", "🔥"
        LIKE = "👍🏾", "👍🏾"
        SURPRISE = "😯", "😯"
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    author = models.ForeignKey(User, related_name="reactions", null=True, blank=True, on_delete=models.SET_NULL)
    post = models.ForeignKey(MoviePost, related_name="reactions", on_delete=models.CASCADE, null=True)
    ip_address = models.CharField(max_length=200)
    type = models.CharField(max_length=50, choices=Type.choices, default=Type.LIKE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    post = models.ForeignKey(MoviePost, related_name="comments", on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, related_name="comments", null=True, blank=True, on_delete=models.SET_NULL)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Subscriber(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    email = models.EmailField()
    ip_address = models.CharField(max_length=200)

