from django.shortcuts import render,redirect
from django.views.generic import View, CreateView, DetailView ,FormView
from django.views.generic.edit import UpdateView, DeleteView
from .models import Post
from .forms import PostForm, CommentForm
from django.urls import reverse_lazy,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
#با کیو میتونیم عبارت های منطقی مثل اند و اور و نات درست کنیم و کوئری مهمیه
from django.core.paginator import Paginator
from django.views.generic.detail import SingleObjectMixin # بوسیله این میتونیم محتوایی که اتک شده به یک یوار ال رو بگیریم


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


class CommentGet(DetailView):
    model = Post
    template_name = 'single_post.html'


    def get_context_data(self, **kwargs):# متد موجود توی دیتیل ویو . میره دیکشنری کانتکس که اطلاعات موجود برای نمایش توی صفحه داره برای ما استخراج میکنه و میاره تا ما در کنار این اطلاعات فرم کامنت رو نشون بدیم. چون همه چیو داره ولی فرم رو نداره میخواهیم بهش فرم رو بدیم
        context = super().get_context_data(**kwargs)# از سوپر یا دیتیل ویو این متد رو استخراج میکنه و این متد دیکشنری کانتکس رو برای ما مقدار میده
        context['form'] = CommentForm()# بهش میگیم توی کانتکس یه مقدار یا فیلد جدید بهش اضافه کن یعنی به همه ی محتوای پست حالا فرم رو هم اضافه کن و از کامنت فرم اون فرم رو بگیر
        return context
        #این کلاس مسئول پاسخ دهی به گت ریکوئست هست

class CommentPost(SingleObjectMixin, FormView):#ارث بری چندگانه
    model = Post
    form_class = CommentForm
    template_name = "single_post.html"

    def post(self, request, *args, **kwargs):# پاسخدهی به پست ریکوستا
        self.object = self.get_object() # از سینگل ابجکت میکسین میاد. میره و پست فعلی رو برامون استخراج میکنه و میارهبه عنوان یه ابجکت میزاره اینجا. پس با استفاده از یو ار الی که داشتیم کل محتوا رو ذخیره کردیم توی ابجکت
        return super().post(request, *args, **kwargs) # متد پست کاری که اینجا انجام میره فرمی که از طرف کاربر ارسال شده چک میکنه اگر فرم ولید و درست باشه میاد و تابع فرم ولید رو برای ما اجرا میکنه
    
    def form_valid(self, form):
        comment = form.save(commit=False)#کامیت مساوی با فالس یعنی توی دیتا بیس ذخیره نشه فعلا
        comment.parent_post = self.object# این کامنت یک پست داره و از طریق ابجکت بالایی پیداش میکنیم
        comment.author = self.request.user # نویسنده کامنت رو برمیداریم
        comment.save() # حالا داخل دیتا بیس سیو میشه
        return super().form_valid(form) #متد فرم ولید رو از کلاس سوپر ریترن کن و بهش فرم رو هم بده. فرم ولید کاری که انجام میده اینه که میگه که فرم سیو شد و توی دیتا بیس قرار گرف حالا ساکسس یو ارال رو فراخوانی کن

    def get_success_url(self):
        post = self.get_object()#مقاله فعلی ما
        return reverse("post_detail", kwargs={'pk': post.pk})




#در کلاس پست دیتیل ما دو نوع ریکوئست دریافت میکنیم
class PostDetail(View):
    def get(self, request, *args,**kwargs ):#اور راید متد گت ویو . اگر ارگومان  های دیگه اومد.
        view = CommentGet.as_view()
        return view(request, *args,**kwargs)
        # به این ترتیب اگر گت ریکوئست براش بیاد میتونه پاسخ دهی بکنه
        
    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)




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