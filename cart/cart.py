from django.conf import settings
from catshop import models
from decimal import Decimal
import json

class Cart:

    def __init__(self, request):
        self.session = request.session #سیشن ریکوئست رو بگیره متغیر کنه

        self.request = request #گرفتن یوزر برای پیاده سازی ذخیره سبد

        cart = self.session.get(settings.CART_SESSION_ID) #گرفتن سیشن سبد خریداگه وجود 
        if not cart:#اگه این سبد خرید توی سیشنها نبود
            cart = self.session[settings.CART_SESSION_ID] = {}  #سیشن یه کی ولیو عه
        self.cart = cart

    def add(self, product, product_count=1, update_count=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'product_count':0,
                                     'price':str(product.price)}

        product_count = int(product_count)    

        if update_count:
            self.cart[product_id]['product_count']=product_count
        else:
            self.cart[product_id]['product_count'] += product_count #اگه اپدیت نکرده بهش همون پیش فرضو اضافه کن  که مقدار پیش فرض یکه. در واقع این برای اضافه کردن دو باره به سبده
        self.save()

    def save_to_profile(self, user):
        #ذخیره سبد خرید در پروفایل کاربر
        if user.is_authenticated:
            profile = user.profile
            profile.old_cart = json.dumps(self.cart)  # تبدیل سبد خرید به جیسون
            profile.save()


    def load_from_profile(self, user):
        #بارگذاری سبد خرید از پروفایل کاربر
        if user.is_authenticated:
            profile = user.profile
            if profile.old_cart:
                self.cart = json.loads(profile.old_cart)  # تبدیل جیسون به دیکشنری
                self.save()  # ذخیره در سشن
          

        
    
    def remove(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()


  
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    
    def __iter__(self):#هر کلاسی اینو داشته باشه ایتر ایبل هست و دیتا ما مثل لیست میشه و میتونیم توش فوریچ بزنیم و دیتامونو بگیریم
        product_ids = self.cart.keys()
        products = models.Product.objects.filter(id__in=product_ids)
        
        for product in products:
            cart_item = self.cart[str(product.id)] #ایجاد محصولات برای حساب هزینه

            if product.is_sale:
                cart_item['price'] = Decimal(product.sale_price)

            else:
                cart_item['price'] = Decimal(product.price)

            cart_item['product'] = product

            cart_item['total_price'] = cart_item['price'] * cart_item['product_count']

            yield cart_item #دیگه نمیاد همه حلقه رو لوپ بزنه بعد نتیجه رو بما بده . اون چیزی که میخوایم اون لحظه ریکوئست مارو جواب میده . برای لیزی لودینگ ازش استفاده میشه . برای وقتایی که یه لیست خیلی بزرگ داشته باشیم و... ا


    def __len__(self):
        # تعداد کل محصولات در سبد خرید را برمی‌گرداند
        return sum(item['product_count'] for item in self.cart.values())



    def get_total_price(self):
        return sum( Decimal(item['price']) * item['product_count'] for item in self.cart.values())