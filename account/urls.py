from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns=[
    #path('login/',views.user_login,name='login'),
    # path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    # path('logout/',auth_views.LogoutView.as_view(template_name='logout.html'),name='logout'),
    path('login/',views.userlogin,name='login'),
    path('logout/',views.userlogout,name='logout'),
    path('register/',views.register,name='register'),
]