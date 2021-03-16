# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 13:43:37 2020

@author: Johnny_Huang
"""
import requests,json
from datetime import datetime

class api_get_data():

    def __init__(self):
        self.get_time=self.get_date_time()
        get_Token=self.api_getAuthentication()
        self.CATR_data=self.api_crawler("486",get_Token,self.get_time)
        self.Aten_data=self.api_crawler("490",get_Token,self.get_time)

    def get_date_time(self):
        x = datetime.now()
        return [x.year,x.month,x.day]

    def api_getAuthentication(self):
        url = "http://172.16.201.48/booked/Web/Services/Authentication/Authenticate"
        # remember to chamge the password
        payload="{\"username\":\"20000463\",\"password\":\"398JZU@@@@\"}\r\n"
        headers = {
          'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        params = json.loads(response.text)
        return [params["sessionToken"],params["userId"]]

    def api_crawler(self,chamber,Token,time):
        url = "http://172.16.201.48/booked/Web/Services/index.php/Reservations/?resourceId="+chamber+"&startDateTime="+str(time[0])+"-"+str(time[1])+"-01T00:00:0&endDateTime="+str(time[0])+"-"+str(time[1])+"-"+str((time[2]))+"T24:00:00"
        # url = "http://172.16.201.48/booked/Web/Services/index.php/Reservations/?resourceId="+chamber+"&startDateTime=2020-11-1&endDateTime="+str(time[0])+"-"+str(time[1])+"-"+(str(time[2]+1))
        # url = "http://172.16.201.48/booked/Web/Services/index.php/Reservations/?resourceId="+chamber+"&startDateTime=2020-11-1T00:00:00&endDateTime=2020-11-30T24:00:00"
        payload="{\"username\" :\"20000463\", \"password\":\"398JZU@@@\"}"
        headers = {
          'X-Booked-Userid': Token[1],
          'X-Booked-SessionToken': Token[0],
          'Content-Type': 'application/json'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        params = json.loads(response.text)

        # return params["reservations"]
        # print(len(params["reservations"]))
        list_data=[]
        for i in params["reservations"]:
            url = "http://172.16.201.48/booked/Web/Services/index.php/Reservations/"+i["referenceNumber"]
            payload={}
            response = requests.request("GET", url, headers=headers, data=payload)
            params = json.loads(response.text)
            hours=self.time_calculate(params["startDate"],params["endDate"])
            BUdata={}
            BUdata={"resources":params["resources"][chamber]["name"],"開始":params["startDate"],
                    "結束":params["endDate"],"Hours":int(hours),"用戶":params["owner"]["firstName"],
                    "models":params["customAttributes"][1]["value"],"Project":params["customAttributes"][3]["value"],"BU":params["customAttributes"][0]["value"]}
            list_data.append(BUdata)
        return list_data

    # https://blog.csdn.net/yuhentian/article/details/78167440
    # https://codertw.com/%E7%A8%8B%E5%BC%8F%E8%AA%9E%E8%A8%80/370349/
    def time_calculate(self,startday,endday):
        startday=startday.split("+",1)[0]
        endday=endday.split("+",1)[0]
        ind_start=datetime.strptime(startday,"%Y-%m-%dT%H:%M:%S")
        ind_end=datetime.strptime(endday,"%Y-%m-%dT%H:%M:%S")
        time_sum=(ind_end-ind_start).total_seconds()/60/60
        return time_sum

if __name__=='__main__':
    get_api=api_get_data()
    # get_Token=api_getAuthentication()
    # CATR_data=api_crawler("486",get_Token)
    # Aten_data=api_crawler("490",get_Token)
