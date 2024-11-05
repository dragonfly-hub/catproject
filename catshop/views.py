from django.shortcuts import redirect, render
from .models import Product,Category 
from django.contrib import messages
from cart.forms import CartAddProductForm


def catshop_home(request):
    all_products = Product.objects.all()
    return render(request , 'catshop_home.html',{'products':all_products})


def product(request,pk):
    product = Product.objects.get(id=pk)
    cart_add_product_form = CartAddProductForm()
    return render(request , 'product.html',{'product':product, 'cart_add_product_form':cart_add_product_form})


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