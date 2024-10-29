from django.urls import path
from . import views

urlpatterns = [
    path('', views.catshop_home, name='catshop_home'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:cat>', views.category, name='category'),
]