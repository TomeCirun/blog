from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse
from ckeditor.fields import RichTextField
from PIL import Image


class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to="pics/", null=True, blank=True)
    image_url = models.CharField(max_length=500, default=None, null=True, blank=True)
    overview = RichTextField()
    content = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    published = models.BooleanField(default=True)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def save_img(self):
        img = Image.open(self.thumbnail.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.thumbnail.path)

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})
