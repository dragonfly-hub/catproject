from django.db import models
from catshop.models import Category as Catshop_Category

class Category(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=500, default='', blank=True, null=True)#خالی یا نال بود خطا نده و اوکی باشه 
    picture = models.ImageField(upload_to='upload/catcategory/', blank=True, null=True )

    def __str__(self):
        return self.name


class Cat(models.Model):
    name = models.CharField(max_length=50)
    personality = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    eyes_and_fur = models.CharField(max_length=200)
    activity = models.CharField(max_length=300)
    health = models.CharField(max_length=300)
    maintenance = models.CharField(max_length=300)
    feeding = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default= 1 )# این گربه حذف شد مدل کتگوریش باقی بماند و اگر دسته بندی انتخاب نکردیم توی اولین دسته قرار بگیره
    picture = models.ImageField(upload_to='upload/cat/')#در این مسیر اپلود شه
    

    product_category = models.ManyToManyField(Catshop_Category) 


    def __str__(self):
        return self.name
    

class Related_Products_For_Cat(models.Model):
    category = models.ForeignKey(Catshop_Category, on_delete=models.CASCADE) 
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
    
    
    


