from django.contrib import admin
from . import models


# Register your models here.
# مدل هارا به پنل ادمین اضافه میکنیم
class Related_Product_Inline(admin.TabularInline):
    model = models.Related_Products_For_Cat
    extra = 1

class CatAdmin(admin.ModelAdmin):
    inlines = (Related_Product_Inline,)


admin.site.register(models.Category)
admin.site.register(models.Cat, CatAdmin)
admin.site.register(models.Related_Products_For_Cat)




