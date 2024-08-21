from django.contrib import admin
from .models import Reaction, Category, MoviePost, Subscriber, Comment

# Register your models here.

class MoviePostAdmin(admin.ModelAdmin):
    list_display = ["movie_name"]

admin.site.register(Category)
admin.site.register(MoviePost, MoviePostAdmin)
admin.site.register(Reaction)
admin.site.register(Comment)
admin.site.register(Subscriber)