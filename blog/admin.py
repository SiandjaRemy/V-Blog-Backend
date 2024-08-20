from django.contrib import admin
from .models import Reaction, Category, Post, Subscriber, Comment

# Register your models here.

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Reaction)
admin.site.register(Comment)
admin.site.register(Subscriber)