from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .cart import Cart
from catshop import models
from django.views.decorators.http import require_POST
from . import forms


@require_POST
def cart_add(request, product_id):
  cart = Cart(request)
  product = get_object_or_404(models.Product, id=product_id)
  form = forms.CartAddProductForm(stock=product.stock, data=request.POST)
  if form.is_valid():
    form_data = form.cleaned_data
    cart.add(product=product,
             product_count=form_data['product_count'],
             update_count=form_data['update'])
  return redirect(reverse('cart:cart_detail')) # استفاده کردن از فضای نام برای اپلیکیشن

def cart_detail(request):
  cart = Cart(request)
  for item in cart:#میتونیم فور بزنیم چون iterable
    item['update_product_count_form'] = forms.CartAddProductForm(
      stock=item['product'].stock,
      initial={'product_count':item['product_count'],
               'update':True}
    )
  return render(request, 'cart_detail.html', {'cart': cart})

def cart_remove(request, product_id):
  cart = Cart(request)
  product = get_object_or_404(models.Product, id=product_id)
  cart.remove(product)
  return redirect(reverse('cart:cart_detail'))