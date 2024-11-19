from django import forms
from .models import Post, Comment, Profile


class UpdateUserProfile(forms.ModelForm):
    biography = forms.CharField(
         label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':' بیوگرافیِ من'}),
        required=False #الزامی نیست
    )
    photo = forms.ImageField(
         label="",
        widget=forms.ClearableFileInput(attrs={'class':'form-control', 'placeholder':'عکس پروفایلِ من'}),
        required=False #الزامی نیست
    )

    class Meta:
        model = Profile
        fields = ('biography','photo')



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


