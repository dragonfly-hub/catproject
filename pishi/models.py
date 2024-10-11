from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=500, default='', blank=True, null=True)#خالی یا نال بود خطا نده و اوکی باشه 

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
    

    #مکمل های مفید
    vitamin_sup = models.BooleanField(default=False)
    mineral_sup = models.BooleanField(default=False)
    omega_sup = models.BooleanField(default=False)
    probiotic_sup = models.BooleanField(default=False)
    amino_asid_sup = models.BooleanField(default=False)
    herbal_sup = models.BooleanField(default=False) 


    def __str__(self):
        return self.name