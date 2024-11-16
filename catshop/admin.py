from django.contrib import admin
from . import models
from pishi.admin import Related_Product_Inline
from django.contrib.auth.models import User

class CategoryAdmin(admin.ModelAdmin):
    inlines = (Related_Product_Inline,)



admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Customer)
admin.site.register(models.Product)
admin.site.register(models.Order)
admin.site.register(models.Profile)

class ProfileInLine(admin.StackedInline): #اینلاین کردن مدل پروفایل
    model = models.Profile

class UserAdmin(admin.ModelAdmin): # اضافه کردن اینلاین پروفایل به یوزر و ایجاد پنل ادمین شخصی سازی شده
    model = User
    fields = ['username','first_name','last_name','email']
    inlines = [ProfileInLine]


admin.site.unregister(User) 
admin.site.register(User, UserAdmin)