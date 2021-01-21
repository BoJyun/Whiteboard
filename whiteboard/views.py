from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.core import serializers
from .forms import peopleForm,adminForm
from .models import people
import json,datetime
from .nowUser import nowUser,nextUser

# Create your views here.

User=nowUser()
NextUser=nextUser()

def whiteboard(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            form=adminForm(request.POST)
        else:
            form=peopleForm(request.POST)

        if form.is_valid():
            new_one=form.save(commit=False)
            new_one.line_num=len(people.objects.all())+1
            new_one.save()
            return redirect('/whiteboard')

    elif request.user.is_authenticated:
        form=adminForm()
    else:
        form=peopleForm()

    return render(request,'whiteboard.html',{'form':form})

def data_people(request):
    data=list(people.objects.filter(done=False)) #who is not done the measurement
    data2=people.objects.filter(done=True)       #who is done the measurement

    j=0
    for i in range(0,len(data)):  #
        try:
            print(1)
            if data[i].cutline==True:
                temp=data[j]
                data[j]=data[i]
                for k in range(i,j,-1):
                    data[k]=data[k-1]
                data[j+1]=temp
                j+=1
        except IndexError:
            print(i,j)
            continue
    print(data)
    if len(data)==0:
        NextUser.userNam='None'
        NextUser.userEmID=0
        NextUser.userNum=0
        qs='None'
    else:
        qs = serializers.serialize('json', data,fields=('user','employeeID','extension_num','line_num','done','cutline','frequent','circuleNum'))
        qs= json.loads(qs)
        NextUser.userNam=data[0].user
        NextUser.userEmID=data[0].employeeID
        NextUser.userNum=data[0].line_num

    if len(data2)==0:
        qs2='None'
    else:
        qs2 = serializers.serialize('json', data2,fields=('user','employeeID','extension_num','line_num'))
        qs2= json.loads(qs2)

    return JsonResponse({'user':qs,'doneuser':qs2,'nowUserNam':User.userNam,'nowUserNum':User.userNum,'nextUserNam':NextUser.userNam,'nextUserNum':NextUser.userNum})

def authUserlogin(request): #讀卡機報到
    if request.method=='GET':
        userEmID=request.GET['user']
        if userEmID:
            # https://chinese.freecodecamp.org/news/python-is-operator/
            userData=people.objects.filter(employeeID=userEmID,done=False)
            if userData is not None:
                if userData.filter(cutline="True") is not None:
                    now_user=userData.filter(cutline="True").first()
                else:
                    now_user=userData.first()
                User.userNam=now_user.user
                User.userNum=now_user.line_num
                User.userEmID=userEmID
                now_user.done=True
                now_user.save()
                return HttpResponse(json.dumps({"Message":"{id}報到成功".format(id = now_user.user),"nowUserNam":now_user.user,"nowUserNum":now_user.line_num}),"application/json")
        else:
            return HttpResponse(json.dumps({"Message":"您尚未預約或請輸入正確工號"}))

    return HttpResponse(json.dumps({"Message":"Method Error"}))

def authUserlogout(request): #讀卡機刷退
    downTime=datetime.date.today()
    now_user=people.objects.filter(user=User.userNam,employeeID=User.userEmID,line_num=User.userNum)
    now_user.update(done=True,DownTime=downTime)
    User.userNam="None"
    User.userEmID=0
    User.userNum=0

    return HttpResponse(json.dumps({"Message":"刷退成功"}))

def authUserlogquit(request,num):
    quit_user=people.objects.filter(line_num=num).first()
    quit_user.done=True
    quit_user.save()

    return HttpResponse(json.dumps({"Message":"棄單"}))


#https://blog.csdn.net/weixin_42134789/article/details/80520500
#https://blog.csdn.net/weixin_43789195/article/details/106072445
#https://stackoverflow.com/questions/33142395/the-submitted-form-is-not-saved-in-sql-django
#https://www.itread01.com/content/1544604310.html
#https://medium.com/i-am-mike/%E4%BD%BF%E7%94%A8axios%E6%99%82%E4%BD%A0%E7%9A%84api%E9%83%BD%E6%80%8E%E9%BA%BC%E7%AE%A1%E7%90%86-557d88365619
#https://nijialin.com/2020/06/17/python-class-instance-level-diff/
#https://www.itread01.com/content/1546169169.html
#https://codertw.com/%E7%A8%8B%E5%BC%8F%E8%AA%9E%E8%A8%80/360150/