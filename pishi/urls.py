from django.urls import path
from . import views

urlpatterns = [
    path('', views.helloworld, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user , name='login'),
    path('input-email/', views.input_email_for_login , name='input_email_for_login'),
    path('login-email/', views.Login_User_Email.as_view() , name='login_email'),
    path('logout/', views.logout_user , name='logout'),
    path('signup/', views.signup_user , name='signup'),
    path('update_user/', views.update_user , name='update_user'),
    path('update_info/', views.update_info , name='update_info'),
    path('update_password/', views.update_password , name='update_password'),
    path('cat/<int:pk>', views.cat , name='cat'),
    path('cat-category/<str:cat>', views.cat_category , name='cat_category'),
    path('cat-category/', views.cat_categorys , name='cat_categorys'),
    path('cat-related-products/<int:pk>/', views.cat_related_products , name='cat_related_products'),
    path('search/', views.search , name='search'),
]
