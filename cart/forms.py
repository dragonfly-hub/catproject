from django import forms

PRODUCT_COUNT_CHOICES = [ (i, str(i)) for i in range(1, 6)]

class CartAddProductForm(forms.Form):
    product_count = forms.TypedChoiceField(choices=PRODUCT_COUNT_CHOICES,coerce=int, label='تعداد')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)#پیش فرض داشته باشه و  کاربر لازم نداشته باشه واردش کنه