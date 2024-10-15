from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

def catlog_home(request):
    return render(request,'catlog_home.html')


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