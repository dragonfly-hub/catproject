from typing import Any
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from .models import Cat, Category, Related_Products_For_Cat
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm, UpdateUserForm, UpdatePasswordForm, UpdateUserInfo
from django.views import generic
from random import randint
from catshop.models import Product, Profile
from django.db.models import Q
from payment.forms import ShippingForm
from payment.models import ShippingAddress,Order,OrderItem


def helloworld(request):
    all_cats = Cat.objects.all()
    return render(request, 'index.html', {'cats':all_cats})
    


def about(request):
    return render(request, 'about.html')



def login_user(request):
    if request.method == "POST":
      username = request.POST['username']
      password = request.POST['password']

      user = authenticate(request, username=username, password=password)

      if user is not None:
           login(request, user)
           messages.success(request, ("با موفقیت وارد شدید"))
           return redirect("home")
      else:
           messages.success(request, (" مشکلی در لاگین وجود داشت"))
           return redirect("login")
    else:    
        return render(request, 'login.html')



def input_email_for_login(request):
     return render(request, 'input_email_for_login.html', {})




class Login_User_Email(generic.TemplateView):
    otp = ''
    email = ''
    attempt_count = 0  # شمارش تلاش‌های ورود ناموفق
    
    def get(self, request, *args, **kwargs):
        Login_User_Email.email = request.GET.get('email')
        
        Login_User_Email.otp = str(randint(100000,999999))
        Login_User_Email.attempt_count = 0  # ریست شمارش تلاش‌ها

        messages.success(request, Login_User_Email.otp)
        return render(request, 'login_with_email.html')
    
    def post(self, request, *args, **kwargs):
        sent_otp = request.POST.get('sent-otp')
        if sent_otp == Login_User_Email.otp:
            user =get_user_model().objects.filter(email=Login_User_Email.email).first()
            #گت یوزر مدل چیکار میکنه؟اگر کاستوم یوزر تعریف کرده باشیم میاد اون کاستوم یوزر هارو میاره اگه تعریف نکرده باشیم مال جنگو رو میاره.متد فیلتر از متد گت مناسب تره اگه گت چیزی پیدا نکنه ارور میده ولی فیلتر نه میگه صفر تا پیدا کرده. فرست میاد از بین اونایی که فیلتر پیدا کرده اون اولیو بما میده که چون یونیک هستن فقط یکی پیدا میکنه اگه وجود داشته باشه
            if user: 
                login(request, user)
                messages.success(request, ("با موفقیت وارد شدید"))
                return redirect("home")
            else:
                messages.success(request, (" چنین اکانتی وجود ندارد. ابتدا حساب کاربری ایجاد کنید"))
                return redirect("login")
        else:
             # اگر کد وارد شده اشتباه باشد
            Login_User_Email.attempt_count += 1
            if Login_User_Email.attempt_count < 2:
                # اجازه تلاش مجدد
                messages.error(request, "کد وارد شده اشتباه است. لطفا مجددا امتحان کنید.")
                return render(request, 'login_with_email.html')
            else:
                # اگر تعداد تلاش‌ها بیشتر از حد مجاز باشد
                messages.error(request, "شما بیش از حد مجاز تلاش کرده‌اید. لطفا دوباره کد جدید دریافت کنید.")
                return redirect("input_email_for_login")





def logout_user(request):
    logout(request)
    messages.success(request, ("با موفقیت خارج شدید!"))
    return redirect('home')


def signup_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password1)
            login(request, user)
            messages.success(request, (" اکانت شما ساخته شد"))
            return redirect("update_info")
        else:
            messages.success(request, (" مشکلی در ثبت نام شما وجود دارد" ))
            return redirect("signup")
    else:
        return render(request, 'signup.html', {'form':form})

def update_user(request):


    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None , instance = current_user)#اطلاعاتی که پست کرده یا نکرده یا از قبل بوده
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request , 'پروفایل شما ویرایش شد')
            return redirect('home')
        return render(request, 'update_user.html',{'user_form':user_form})#فرم هنوز پر نشده
    else:
       messages.success(request , 'ابتدا باید لاگین شوید')
       return redirect('home') 

def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id) #ممکنه ایدی یک مدل یوزر مساوی ایدی یک پروفایل نیس. برای همین
        shippping_user = ShippingAddress.objects.get(user__id = request.user.id)


        form = UpdateUserInfo(request.POST or None , instance = current_user)#اطلاعاتی که پست کرده یا نکرده یا از قبل بوده
        shipping_form = ShippingForm(request.POST or None , instance = shippping_user)


        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()


            messages.success(request , 'اطلاعات کاربری شما ویرایش شد')
            return redirect('home')
        return render(request, 'update_info.html',{'form':form,'shipping_form':shipping_form})#فرم هنوز پر نشده
    else:
       messages.success(request , 'ابتدا باید لاگین شوید')
       return redirect('home') 
    


def update_password(request):

    if request.user.is_authenticated:
        current_user = request.user

        if request.method=='POST':
            form = UpdatePasswordForm(current_user, request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, 'رمز با موفقیت ویرایش شد')
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return redirect('update_password')

        else:
            form = UpdatePasswordForm(current_user)
            return render(request, 'update_password.html',{'form':form})
        
    else:
        messages.success(request , 'باید اول لاگین بشین!')
        return redirect('home')


def cat(request,pk):
    cat = Cat.objects.get(id=pk)
    # پیدا کردن دسته‌بندی‌های مرتبط از طریق Related_Products_For_Cat
    related_categories = Related_Products_For_Cat.objects.filter(cat=cat).values_list('category', flat=True)#ازvalues_list('category', flat=True) استفاده کردیم تا تنها آی‌دی‌های دسته‌بندی‌ها را به صورت یک لیست ساده دریافت کنیم.
    
    related_products = Product.objects.filter(category_id__in=related_categories).distinct()[:4]

    return render(request, 'cat.html', {'cat': cat, 'related_products': related_products})

def cat_related_products(request,pk):
    cat = Cat.objects.get(id=pk)
    related_categories = Related_Products_For_Cat.objects.filter(cat=cat).values_list('category', flat=True)#ازvalues_list('category', flat=True) استفاده کردیم تا تنها آی‌دی‌های دسته‌بندی‌ها را به صورت یک لیست ساده دریافت کنیم.
    
    related_products = Product.objects.filter(category_id__in=related_categories).distinct()

    return render(request, 'cat_related_products.html', {'cat': cat, 'related_products': related_products})

def cat_category(request,cat):
    cat = cat.replace("-"," ")
    try:
        category = Category.objects.get(name=cat)
        cats = Cat.objects.filter(category=category)
        return render(request, 'cat_category.html', {'cats':cats, 'category':category})
    except:
       messages.success(request, ("دسته بندی وجود ندارد" ))
       return redirect("home")



def cat_categorys(request):


    all_cat = Category.objects.all()
    return render(request, 'cat_categorys.html', {'categorys':all_cat})

def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        searched_cat = Cat.objects.filter(Q(name__icontains=searched) | Q(personality__icontains=searched) | Q(country__icontains=searched) | Q(eyes_and_fur__icontains=searched) | Q(activity__icontains=searched)) 
        searched_product =  Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))

        if not searched_cat.exists() and not searched_product.exists():
             messages.success(request, ("نتیجه ای برای جستجوی شما یافت نشد"))
             return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched_cat':searched_cat ,'searched_product':searched_product})
    
    return render(request, 'search.html', {})

def user_orders(request):
   if request.user.is_authenticated:
        delivered_orders = Order.objects.filter(user=request.user, status='Delivered')
        other_orders = Order.objects.filter(user=request.user).exclude(status='Delivered')

        context = {
            'delivered':delivered_orders,
            'other':other_orders
        }
        return render(request, 'user_orders.html',context )
   else:
     messages.success(request , 'دسترسی به این صفحه امکان پذیر نمیباشد')
     return redirect('home')   

