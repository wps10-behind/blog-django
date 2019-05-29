from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30, db_index=True, unique=True, allow_unicode=True, blank=True)

    class Meta:
        ordering = ['slug']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug

class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=50)
    text = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:index")