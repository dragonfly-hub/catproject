from django.shortcuts import render, redirect
from .models import Cat, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm

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
    return render(request, 'cat.html', {'cat':cat})


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