from django.urls import path
from . import views

urlpatterns = [
    path('', views.helloworld, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user , name='login'),
    path('input-email/', views.input_email_for_login , name='input_email_for_login'),
    path('logout/', views.logout_user , name='logout'),
    path('login-email/', views.Login_User_Email.as_view() , name='login_email'),
    path('logout/', views.logout_user , name='logout'),
    path('signup/', views.signup_user , name='signup'),
    path('cat/<int:pk>', views.cat , name='cat'),
    path('cat-category/<str:cat>', views.cat_category , name='cat_category'),
    path('cat-category/', views.cat_categorys , name='cat_categorys'),
]
