from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.core import serializers
from .forms import peopleForm,adminForm
from .models import people
import json,datetime
# from .nowUser import nowUser,nextUser
import threading
import socket
from .tcpserver import ThreadTCPserver,Handler_TCPServer

# Create your views here.
def MyTCP():
    tcp_server=ThreadTCPserver(("127.0.0.1",8001),Handler_TCPServer)
    tcp_server.serve_forever()


def DayTime():
    x=datetime.datetime.now()
    return [x.year,x.month,x.day]

# def TCPreader():
#     print("123")
#     server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#     bind_ip="127.0.0.1"
#     bind_port=8001
#     server.bind((bind_ip,bind_port))
#     server.listen(2)

#     while True:
#         try:
#             print('wait for connecting ...')
#             client,addr=server.accept()
#             print('Connected by ',addr)
#             try:
#                 while True:
#                     print(3)
#                     data=client.recv(1024)
#                     print("Client recv data: ",data)
#                     print(4)
#                     if data==" ":
#                         client.send(bytes("please send the message.","utf-8"))
#                     else:
#                         client.send(bytes("server received you message.","utf-8"))
#                     print(5)
#             except Exception as e:
#                 print(1)
#                 print(e)
#         except Exception as e:
#             print(2)
#             print(e)
# read_t=threading.Thread(target=TCPreader)
# read_t.start()
# User=nowUser()
# NextUser=nextUser()

class USER_TYPE():
    def __init__(self):
        self.NowUser_name="None"
        self.NowUser_EmployeeID=0
        self.NowUser_ExtensionNum=0
        self.NextUser_name="None"
        self.NextUser_EmployeeID=0
        self.NextUser_ExtensionNum=0

User_Type=USER_TYPE()
# CardReader=threading.Thread(target=MyTCP)
# CardReader.start()

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

    if request.user.is_authenticated:
        form=adminForm()
    else:
        form=peopleForm()

    return render(request,'whiteboard.html',{'form':form})

def data_people(request):
    t=DayTime()
    day=str(t[0])+"-"+str(t[1])+"-"+str(t[2])
    data=list(people.objects.filter(done=False)) #who is not done the measurement
    data2=people.objects.filter(done=True,DownTime=day) #who is done the measurement

    j=0
    for i in range(0,len(data)):
        try:
            if data[0].cutline==True and i==0:
                continue
            if data[i].cutline==True:
                temp=data[j]
                data[j]=data[i]
                for k in range(i,j,-1):
                    data[k]=data[k-1]
                data[j+1]=temp
                j+=1
        except Exception as e:
            continue

    if len(data)==0:
        User_Type.NextUser_name='None'
        User_Type.NextUser_EmployeeID=0
        User_Type.NextUser_ExtensionNum=0
        qs='None'
    else:
        qs = serializers.serialize('json', data,fields=('user','employeeID','extension_num','line_num','done',
        'cutline','frequent','circuleNum'))
        qs= json.loads(qs)
        User_Type.NextUser_name=data[0].user
        User_Type.NextUser_EmployeeID=data[0].employeeID
        User_Type.NextUser_ExtensionNum=data[0].line_num

    if len(data2)==0:
        qs2='None'
    else:
        qs2 = serializers.serialize('json', data2,fields=('user','employeeID','extension_num','line_num'))
        qs2= json.loads(qs2)
    # print(request.user)
    return JsonResponse({'user':qs,'doneuser':qs2,'nowUserNam':User_Type.NowUser_name,'nowUserNum':User_Type.NowUser_ExtensionNum,
    'nextUserNam':User_Type.NextUser_name,'nextUserNum':User_Type.NextUser_ExtensionNum,'logUser':str(request.user)})

def authUserlogin(request): #讀卡機報到
    if request.method=='GET':
        userEmID=request.GET['user']
        if userEmID:
            # https://chinese.freecodecamp.org/news/python-is-operator/
            userData=people.objects.filter(employeeID=userEmID,done=False)
            if userData is not None:
                if userData.filter(cutline="True").first() is not None:
                    now_user=userData.filter(cutline="True").first()
                else:
                    now_user=userData.first()
                User_Type.NowUser_name=now_user.user
                User_Type.NowUser_ExtensionNum=now_user.line_num
                User_Type.NowUser_EmployeeID=userEmID
                now_user.done=True
                now_user.save()
                return HttpResponse(json.dumps({"Message":"{id}報到成功".format(id = User_Type.NowUser_name),"nowUserNam":User_Type.NowUser_name,
                "nowUserNum":User_Type.NowUser_ExtensionNum}),"application/json")
        else:
            return HttpResponse(json.dumps({"Message":"您尚未預約或請輸入正確工號"}))

    return HttpResponse(json.dumps({"Message":"Method Error"}))

def authUserlogout(request): #讀卡機刷退
    downTime=datetime.date.today()
    now_user=people.objects.filter(user=User_Type.NowUser_name,employeeID=User_Type.NowUser_EmployeeID,line_num=User_Type.NowUser_ExtensionNum)
    now_user.update(done=True,DownTime=downTime)
    User_Type.NowUser_name="None"
    User_Type.NowUser_ExtensionNum=0
    User_Type.NowUser_EmployeeID=0

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