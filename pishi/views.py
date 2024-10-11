from django.shortcuts import render, redirect
from .models import Cat
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


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
