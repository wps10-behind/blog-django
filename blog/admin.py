from django.contrib import admin

# Register your models here.
from .models import Category, Post
class CategoryOtion(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryOtion)

class PostOption(admin.ModelAdmin):
    list_display = ['category', 'author', 'title', 'text', 'created', 'update', ]

admin.site.register(Post, PostOption)