from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from .models import Cat, Category, Related_Products_For_Cat
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm
from django.views import generic
from random import randint
from catshop.models import Product




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
    
    def get(self, request, *args, **kwargs):
        Login_User_Email.email = request.GET.get('email')
        
        Login_User_Email.otp = str(randint(100000,999999))
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
            messages.success(request, (" کد وارد شده اشتباه است. مجدد امتحان کنید"))
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
            return redirect("home")
        else:
            messages.success(request, (" مشکلی در ثبت نام شما وجود دارد" ))
            return redirect("signup")
    else:
        return render(request, 'signup.html', {'form':form})



def cat(request,pk):
    cat = Cat.objects.get(id=pk)
    # پیدا کردن دسته‌بندی‌های مرتبط از طریق Related_Products_For_Cat
    related_categories = Related_Products_For_Cat.objects.filter(cat=cat).values_list('category', flat=True)#ازvalues_list('category', flat=True) استفاده کردیم تا تنها آی‌دی‌های دسته‌بندی‌ها را به صورت یک لیست ساده دریافت کنیم.
    
    related_products = Product.objects.filter(category_id__in=related_categories).distinct()

    return render(request, 'cat.html', {'cat': cat, 'related_products': related_products})


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