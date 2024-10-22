from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['cat_name','title','excerpt','body','date','picture'] 


        labels = {
            'cat_name': ' نام پیشی محترم را وارد کنید',   
            'title': 'عنوان پست',
            'excerpt': 'خلاصه ای از پست', 
            'body': 'متن پست', 
            'date': ' تاریخ ایجاد پست',
            'picture': ' لطفا یک تصویر برای پست خود انتخاب کنید ',      
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields =['body']
