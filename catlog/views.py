from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class CatlogHome(ListView):
    model = Post # مدل پست رو بردار به این تمپلیت ارسال کن . از نوع لیست است
    template_name = 'catlog_home.html'  #ما نیاز داریم یک لیستی رو ببینیم


class PostDetail(DetailView):
    model = Post
    template_name = 'single_post.html'
        


class NewPost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'new_post.html'
    form_class = PostForm
    success_url = reverse_lazy('catlog')


      # بازنویسی متد form_valid برای تنظیم نویسنده و افزودن پیام موفقیت
    def form_valid(self, form):
        form.instance.writer = self.request.user  # تنظیم نویسنده به کاربر احراز هویت شده
        messages.success(self.request, 'پست شما با موفقیت ایجاد شد!')  # پیام موفقیت
        return super().form_valid(form)
    

class UpdatePost(UpdateView):
     model = Post
     template_name = 'update_post.html'
     fields = ['cat_name','title','excerpt','body','picture']

     def form_valid(self, form):
        messages.success(self.request, 'پست با موفقیت ویرایش شد!')
        return super().form_valid(form)




class DeletePost(DeleteView):
     model = Post
     template_name = 'delete_post.html'
     success_url = reverse_lazy('catlog') 

     def form_valid(self, form):
        messages.success(self.request, 'پست با موفقیت حذف شد!')
        return super().form_valid(form)