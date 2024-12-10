from django.shortcuts import redirect, render
from .models import Product,Category 
from django.contrib import messages
from cart.forms import CartAddProductForm
import random


def catshop_home(request):
    all_products = Product.objects.all()
    new_products = Product.objects.filter(stock__gt=0).order_by('-id')[:4]  # فقط محصولات با موجودی > 0
    return render(request , 'catshop_home.html',{'products':all_products,'new_products': new_products})


def product(request,pk):
    product = Product.objects.get(id=pk)
    cart_add_product_form = CartAddProductForm(stock=product.stock)
    related_products_category = product.category
     # انتخاب محصولات مرتبط در همان دسته‌بندی و حذف محصول اصلی از لیست
    related_products = Product.objects.filter(category=related_products_category).exclude(id=product.id)
     # انتخاب تصادفی چهار محصول مرتبط
    related_products = random.sample(list(related_products), min(4, len(related_products)))
    
    return render(request , 'product.html',{'product':product, 'cart_add_product_form':cart_add_product_form,'related_products':related_products, 'stock': product.stock})


def category(request,cat):
    cat = cat.replace("-"," ")
    # برای اینکه اگر کسی دسته بندی ناموجودی وارد کرد خیلی به خطای عجیب غریبی نخوریم از ترای اگسپت استفاده میکنم
    try:
        category = Category.objects.get(name=cat)
        products = Product.objects.filter(category=category)
        return render(request , 'catshop_category.html',{'products':products,'category':category})
    except:
        messages.success(request,("دسته بندی وجود ندارد"))
        return redirect("catshop_home")
    

def category_summary(request):
    all_cat = Category.objects.all()
    return render(request , 'category_summary.html',{'category':all_cat})