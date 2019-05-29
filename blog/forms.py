from django import forms
from .models import Category, Post

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'text']

