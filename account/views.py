from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from .forms import LoginForm
# Create your views here.

from .forms import MyUserCreationForm
def register(request):
    if request.method=='POST':
        user_form=MyUserCreationForm(request.POST)
        if user_form.is_valid():
            new_user=user_form.save(commit=False) #先創建一個空的對象
            print(user_form.cleaned_data)
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()
            return render(request,'account/register_done.html')
    else:
        user_form=MyUserCreationForm()
    return render(request,'account/register.html',{'user_form':user_form})

def userlogin(request):
    if request.user.is_authenticated:
        return redirect('/whiteboard/') #/whiteboard/ mean http:local/whiteboard/
    elif request.method=='POST':        # whiteboard/ mean http:local/app/whiteboard/
        Inform=LoginForm(request.POST)
        if Inform.is_valid():
            cd=Inform.cleaned_data
            print(cd)
            user=authenticate(request,username=cd['username'],password=cd['password'])
            print(user)
            print(type(user))
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('/whiteboard/')
                else:
                    return HttpResponse('Disable account')
            else:
                return HttpResponse('Invalid Login')
    else:
        Inform=LoginForm()
        return render(request,'account/login.html',{'form':Inform})

def userlogout(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request,'account/logout.html')
    else:
        return redirect('/account/login/')