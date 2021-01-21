from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name='app_whiteboard'
urlpatterns=[
    path('',views.whiteboard,name='whiteboard'),

    path('api/lineboard/',views.data_people,name='lineboard'),
    path('api/authUser/login',views.authUserlogin,name='authUserlogin'),
    path('api/authUser/logout',views.authUserlogout,name='authUserlogout'),
    path('api/authUser/logquit/<int:num>/',views.authUserlogquit,name='authUserlogquit'),

]