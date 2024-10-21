from django.shortcuts import render,redirect
from django.views.generic import View, CreateView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
#با کیو میتونیم عبارت های منطقی مثل اند و اور و نات درست کنیم و کوئری مهمیه
from django.core.paginator import Paginator


class CatlogHome(View):
    model = Post # مدل پست رو بردار به این تمپلیت ارسال کن . از نوع لیست است
    template_name = 'catlog_home.html'  #ما نیاز داریم یک لیستی رو ببینیم
    paginate_by = 2

    def get(self,request):
        posts = Post.objects.all()
        paginator = Paginator(posts, self.paginate_by)#  همه پست هارو میخونه  و براساس اینکه گفتیم چندتا چندتا تویه صفحه قرار بده یه شی به نام پجینیتور میسازه. پس پجینیتور ما شامل یه تعداد صفحه میشه که تو هر صفحه یه تعداد پست قرار گرفته

        page_number = request.GET.get('page')# شماره صفحه . به سراغ ریکوئست کاربر از نوع گت میریم . پیج را ازش استخراج میکنیم این پیج از طریق همون ریکوئست کاربر بما میرسع و میفرسته
        page_obj = paginator.get_page(page_number) #با متد گت پیج برو  شماره پیجی که کاربر میخواد استخراج کن بریز تو این

        context = {
            'post_list': page_obj
        }
        return render(request, self.template_name, context )


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
     

def search_catlog(request):
    if request.method == 'POST':
       searched_catlog = request.POST['searched-catlog']
       searched_catlog = Post.objects.filter(Q(cat_name__icontains=searched_catlog) | Q(title__icontains=searched_catlog) | Q(excerpt__icontains=searched_catlog) | Q(body__icontains=searched_catlog))#icontains یعنی به حروف بزرک و کوچیک حساس نباش
       
       if not searched_catlog:
          messages.success(request, ("نتیجه ای یافت شد "))
          return redirect("catlog") 
       else:
          return render(request, 'search_catlog.html',{'searched_catlog':searched_catlog})