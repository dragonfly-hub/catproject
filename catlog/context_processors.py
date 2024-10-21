from .models import Post

def recent_posts(request):
    recent_posts = Post.objects.order_by('-date')[:4]
    #به مدل پست سر میزنم تمام ابجکت هاشو برمیدارم  مرتبشون میکنم به ترتیب دیت یا تاریخ و 5 تای اولشونو برمیدارم
    return {'recent_posts':recent_posts}