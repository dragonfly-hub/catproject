from django.contrib import admin
from . import models
from pishi.admin import Related_Product_Inline

class CategoryAdmin(admin.ModelAdmin):
    inlines = (Related_Product_Inline,)



admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Customer)
admin.site.register(models.Product)
admin.site.register(models.Order)
