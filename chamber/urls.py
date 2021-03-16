from django.urls import path
from . import views

urlpatterns=[
    #path('login/',views.user_login,name='login'),
    path('',views.get_home),

    path('BG',views.get_BG,name='get_BG'),
    path('AllBG/',views.call_AllBG,name='call_AllBG'),
    path('BG_data/<str:resq_BG>/',views.call_BG,name='call_BG'),
]