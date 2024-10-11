from django.contrib import admin
from . import models

# Register your models here.
# مدل هارا به پنل ادمین اضافه میکنیم

admin.site.register(models.Category)
admin.site.register(models.Cat)
