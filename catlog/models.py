from django.db import models
from datetime import date
from django.contrib.auth.models import User

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
