from django import forms


class CartAddProductForm(forms.Form):
    product_count = forms.TypedChoiceField(coerce=int, label='تعداد')
    #product_count = forms.TypedChoiceField(choices=PRODUCT_COUNT_CHOICES,coerce=int, label='تعداد')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)#پیش فرض داشته باشه و  کاربر لازم نداشته باشه واردش کنه

    def __init__(self, stock, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_count'].choices = [(i, str(i)) for i in range(1, stock + 1)]

        #در این فرم، product_count بر اساس موجودی stock تنظیم می‌شود.