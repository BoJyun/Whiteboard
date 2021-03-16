from django.shortcuts import render
from .sort import BGclass
import pandas as pd
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
from datetime import datetime
from .cawler import api_get_data

# df=pd.read_csv(r'D:\\python\\python_django\\chamber\\BG\\chamber.csv',encoding='Big5')
class chamber_data():
    get_api=api_get_data()
    catr_api_data=get_api.CATR_data
    Aten_api_data=get_api.Aten_data
    time_now=get_api.get_time
    BG_sas=BGclass(catr_api_data,Aten_api_data,['SAS_JER500'])
    BG_ais=BGclass(catr_api_data,Aten_api_data,["AIC_T50000","ICS_T30000","SMA_T20000"])
    BG_ch=BGclass(catr_api_data,Aten_api_data,["CH1_H60000","CH2_H50000","CH3_H70000"])
    BG_nw=BGclass(catr_api_data,Aten_api_data,["NW1_D10000","NW2_D20000","NW3_D30000"])
    BG_atd=BGclass(catr_api_data,Aten_api_data,['JN0000'])


def get_today_time():
    x = datetime.now()
    return [x.year,x.month,x.day]

# @login_required
def get_home(request):
    print(request.user)
    return render(request,'chamber/index.html')

# @login_required
def get_BG(request):
    print(request.user)
    return render(request,'chamber/BU.html')

# https://django.cowhite.com/blog/working-with-url-get-post-parameters-in-django/
def call_AllBG(request):
    print(request.user)
    today_time=get_today_time()
    if chamber_data.time_now!=today_time:
        chamber_data()
    else:
        pass

    CATR={}
    CATR['SAS']=chamber_data.BG_sas.CATR_sum
    CATR['AIS']=chamber_data.BG_ais.CATR_sum
    CATR['CH']=chamber_data.BG_ch.CATR_sum
    CATR['NW']=chamber_data.BG_nw.CATR_sum
    CATR['ATD']=chamber_data.BG_atd.CATR_sum
    Aten_5G={}
    Aten_5G['SAS']=chamber_data.BG_sas.Aten5G_sum
    Aten_5G['AIS']=chamber_data.BG_ais.Aten5G_sum
    Aten_5G['CH']=chamber_data.BG_ch.Aten5G_sum
    Aten_5G['NW']=chamber_data.BG_nw.Aten5G_sum
    Aten_5G['ATD']=chamber_data.BG_atd.Aten5G_sum
    Aten_4G={}
    Aten_4G['SAS']=chamber_data.BG_sas.Aten4G_sum
    Aten_4G['AIS']=chamber_data.BG_ais.Aten4G_sum
    Aten_4G['CH']=chamber_data.BG_ch.Aten4G_sum
    Aten_4G['NW']=chamber_data.BG_nw.Aten4G_sum
    Aten_4G['ATD']=chamber_data.BG_atd.Aten4G_sum

    return JsonResponse({'CATR':CATR,'Aten_5G':Aten_5G,'Aten_4G':Aten_4G,'time':chamber_data.time_now})

def call_BG(request,resq_BG):
    print(request.user)
    print(resq_BG)

    today_time=get_today_time()
    if chamber_data.time_now!=today_time:
        chamber_data()
    else:
        pass

    if resq_BG=="SAS":
        BG=chamber_data.BG_sas
    elif resq_BG=="AIS":
        BG=chamber_data.BG_ais
    elif resq_BG=="CH":
        BG=chamber_data.BG_ch
    elif resq_BG=="NW":
        BG=chamber_data.BG_nw
    elif resq_BG=="ATD":
        BG=chamber_data.BG_atd
    else:
        return JsonResponse({'BU':'None'})

    # print(BG.bu_list)
    # print(BG.catr+BG.aten_5G+BG.aten_4G)
    # print(type(BG.sort_df.to_dict('records')))
    return JsonResponse({'BG_list':BG.bu_list,'BG_time':BG.BU,'BG_data':BG.catr+BG.aten_5G+BG.aten_4G,'time':chamber_data.time_now})

chamber_data()