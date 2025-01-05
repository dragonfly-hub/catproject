from decimal import Decimal
from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import ShippingForm
from .models import ShippingAddress
from django.contrib import messages




def payment_success(request):
    return render(request, 'payment/payment_success.html',{})


def checkout(request):
    cart = Cart(request)
    cart_items = list(cart)
    
    session_data = []
    for item in cart_items:
        # اضافه کردن هر آیتم به session_data
        session_data.append({
            'product_name': item['product'].name,
            'product_count': item['product_count'],
            'price': item['price'],
            'product_id': item['product'].id  # ذخیره کردن ID به جای شیء
        })

    
    
    
    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html',{'session_data':session_data,'cart':cart, 'shipping_form':shipping_form})
        

    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html',{'session_data':session_data,'cart':cart,'shipping_form':shipping_form})
    

def confirm_order(request):
    if request.POST:

        # دریافت داده‌های محصولات از فرم
        product_ids = request.POST.getlist('product_ids[]')
        product_names = request.POST.getlist('product_names[]')
        product_counts = request.POST.getlist('product_counts[]')
        prices = request.POST.getlist('prices[]')
    
        # ایجاد لیست cart از داده‌های دریافتی
        cart_final = []
        total_price = 0  # متغیر برای ذخیره قیمت کل

        for i in range(len(product_ids)):
            product_count = int(product_counts[i])  # تبدیل تعداد به عدد صحیح
            price = float(prices[i])  # تبدیل قیمت به عدد اعشاری
            
            # محاسبه قیمت کل برای هر محصول
            total_price += product_count * price
            
            cart_final.append({
                'product_id': product_ids[i],
                'product_name': product_names[i],
                'product_count': product_count,
                'price': price,
            })
        

        request.session['cart_final']= cart_final
        request.session['total_price']= total_price

        # مشخصات ارسال که در صفحه قبل نوشته و پست شده یه دیکشنری خواهد بود
        shipping_form  = ShippingForm(request.POST)

        if shipping_form.is_valid():
            # تبدیل داده‌های فرم به دیکشنری
            user_shipping = shipping_form.cleaned_data

        request.session['user_shipping']= user_shipping
        


        # ارسال داده‌ها به تمپلیت
        return render(request, 'payment/confirm_order.html', {
            'cart_final': cart_final,
            'shipping_info': user_shipping,
            'total_price':total_price
            

        })

    else:
        messages.success(request, 'دسترسی به این صفحه امکان پذیر نمیباشد')  # که با سرچ یو ارال نیان تو این صفحه
        return redirect('home')


def proccess_order(request):
    if request.POST:
        pass
    else:
        messages.success(request, 'دسترسی به این صفحه امکان پذیر نمیباشد')  # که با سرچ یو ارال نیان تو این صفحه
        return redirect('home')