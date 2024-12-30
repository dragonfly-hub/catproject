from django.shortcuts import render,redirect
from django.views.generic import View, CreateView, DetailView ,FormView
from django.views.generic.edit import UpdateView, DeleteView
from .models import Post,Profile
from .forms import PostForm, CommentForm, UpdateUserProfile
from django.urls import reverse_lazy,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
#با کیو میتونیم عبارت های منطقی مثل اند و اور و نات درست کنیم و کوئری مهمیه
from django.core.paginator import Paginator
from django.views.generic.detail import SingleObjectMixin # بوسیله این میتونیم محتوایی که اتک شده به یک یوار ال رو بگیریم
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse


class CatlogHome(View):
    model = Post # مدل پست رو بردار به این تمپلیت ارسال کن . از نوع لیست است
    template_name = 'catlog_home.html'  #ما نیاز داریم یک لیستی رو ببینیم
    paginate_by = 2

    def get(self,request):

          # پاک کردن `original_previous_url`
        if 'original_previous_url' in request.session:
            del request.session['original_previous_url']




         # لیست پست‌ها
        posts = Post.objects.all().order_by('-date')
        paginator = Paginator(posts, self.paginate_by)#  همه پست هارو میخونه  و براساس اینکه گفتیم چندتا چندتا تویه صفحه قرار بده یه شی به نام پجینیتور میسازه. پس پجینیتور ما شامل یه تعداد صفحه میشه که تو هر صفحه یه تعداد پست قرار گرفته

        page_number = request.GET.get('page')# شماره صفحه . به سراغ ریکوئست کاربر از نوع گت میریم . پیج را ازش استخراج میکنیم این پیج از طریق همون ریکوئست کاربر بما میرسع و میفرسته
        page_obj = paginator.get_page(page_number) #با متد گت پیج برو  شماره پیجی که کاربر میخواد استخراج کن بریز تو این
           
          # اطلاعات پروفایل کاربر
        user_profile = None
        if request.user.is_authenticated:  # اگر کاربر لاگین باشد
            try:
                user_profile = Profile.objects.get(user=request.user)  # پروفایل کاربر
            except Profile.DoesNotExist:
                user_profile = None  # اگر پروفایل تعریف نشده باشد


         # اضافه کردن تعداد کامنت به هر پست
        posts_with_comments = []
        for post in page_obj:
            post.comment_count = post.comment_set.count()
            posts_with_comments.append(post)



        context = {
            'post_list': page_obj,
            'user_profile': user_profile,
        }
        return render(request, self.template_name, context )
    

    

class CommentGet(DetailView):
    model = Post
    template_name = 'single_post.html'


    def get_context_data(self, **kwargs):# متد موجود توی دیتیل ویو . میره دیکشنری کانتکس که اطلاعات موجود برای نمایش توی صفحه داره برای ما استخراج میکنه و میاره تا ما در کنار این اطلاعات فرم کامنت رو نشون بدیم. چون همه چیو داره ولی فرم رو نداره میخواهیم بهش فرم رو بدیم
        context = super().get_context_data(**kwargs)# از سوپر یا دیتیل ویو این متد رو استخراج میکنه و این متد دیکشنری کانتکس رو برای ما مقدار میده
        post = self.get_object()
        
        context['form'] = CommentForm()# بهش میگیم توی کانتکس یه مقدار یا فیلد جدید بهش اضافه کن یعنی به همه ی محتوای پست حالا فرم رو هم اضافه کن و از کامنت فرم اون فرم رو بگیر
        context['author_profile'] = Profile.objects.get(user=post.writer)
        context['like_count'] = post.total_likes()
        context['catlog_url'] = reverse('catlog')
       
        # ارسال URL اصلی قبلی به قالب
        context['previous_url'] = self.request.session.get('original_previous_url', reverse('catlog'))

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
        
         # ذخیره URL قبلی فقط در درخواست‌های GET
        if not request.session.get('original_previous_url'):
            previous_url = request.META.get('HTTP_REFERER', '')
            request.session['original_previous_url'] = previous_url  # ذخیره در سشن
        
        view = CommentGet.as_view()
        return view(request, *args,**kwargs)
        # به این ترتیب اگر گت ریکوئست براش بیاد میتونه پاسخ دهی بکنه




    def post(self, request, *args, **kwargs):

        # مقدار `original_previous_url` تغییر نمی‌کند

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
       

def update_profile(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UpdateUserProfile(request.POST or None , request.FILES or None, instance = current_user)#اطلاعاتی که پست کرده یا نکرده یا از قبل بوده
        if form.is_valid():
            form.save()
            messages.success(request , 'پروفایل کتلاگـِ شما ویرایش شد')
            return redirect('catlog')
        return render(request, 'update_profile.html',{'form':form ,'profile_photo': current_user.photo})#فرم هنوز پر نشده
    else:
       messages.success(request , 'ابتدا باید لاگین شوید')
       return redirect('catlog') 
    

@receiver(pre_delete, sender=Profile)
def delete_profile_photo(sender, instance, **kwargs):
    if instance.photo:
        instance.photo.delete(False) #این کد تضمین می‌کند که وقتی یک عکس از پروفایل حذف می‌شود، فایل فیزیکی نیز از سیستم حذف شود.


@login_required
def my_posts(request):
    posts = Post.objects.filter(writer=request.user)  # فیلتر کردن پست‌های نوشته شده توسط کاربر
    user_profile = Profile.objects.get(user=request.user)
    context = {
        'posts': posts,
        'user_profile': user_profile,
    }
    return render(request, 'my_posts.html', context)


@login_required
def author_posts(request, author_id):
    author = get_object_or_404(User, id=author_id)
    author_profile = get_object_or_404(Profile, user=author)  # فرض می‌کنیم هر نویسنده یک پروفایل دارد
    posts = Post.objects.filter(writer=author)

    context = {
        'author': author,
        'author_profile': author_profile,
        'posts': posts,
    }
    return render(request, 'author_posts.html', context)


@login_required
def toggle_like(request, pk):
  if request.method == 'POST':
      post = get_object_or_404(Post, pk=pk)
    
    # اگر کاربر قبلاً لایک کرده باشد، حذف می‌شود
      if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
      else:
        post.likes.add(request.user)
        liked = True

    # تعداد لایک‌های پست
      like_count = post.likes.count()
      return JsonResponse({'liked': liked, 'like_count': like_count})
  return JsonResponse({'error': 'Invalid request'}, status=400)