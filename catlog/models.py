from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    cat_name = models.CharField(max_length=50)
    title = models.CharField(max_length=250)
    excerpt = models.TextField(max_length=500, default='', blank=True, null=True)
    body = models.TextField()
    writer = models.ForeignKey(User ,on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    picture = models.ImageField(upload_to='upload/%y/%m/%d')

    def __str__(self):
        return self.title
    

    def get_absolute_url(self):
        return reverse('post_detail',kwargs = {'pk':self.pk})
    #به مدل ما میگه برای هر شی که از این مدل ساخته شد یک یوارال در نظر بگیر
    # و زمانی که ما پست رو اپدیت میکنیم به یوارالی که برای این شی در نظر گرفته شده میتونه ری دایرکت کنه


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(null=False, blank=False)
    date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.body