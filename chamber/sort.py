# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 15:03:03 2020

@author: Johnny_Huang
"""

import pandas as pd
import numpy as np

class FileSort(): #整理file，把要檢視的bu從df裡挑出來
    def __init__(self,catr_api,aten_api,bu):
        self.catr=self.file_sort(catr_api,bu)
        self.aten=self.file_sort(aten_api,bu)
        self.aten_5G,self.aten_4G=self.sortAten(self.aten)

    def sortAten(self,aten):
        aten5G=[];aten4G=[]
        for i in aten:
            if i['models']=='5G Sub6':
                aten5G.append(i)
            elif i['models']=='LTE OTA' or i['models']=='Passive':
                aten4G.append(i)
        return aten5G,aten4G

    def file_sort(self,df,bu):
        data=[]
        for i in df:
            for j in bu:
                if i['BU']==j:
                    data.append(i)
                    break
        return data

class BGclass(FileSort):
    def __init__(self,catr_api,aten_api,bu):
        super().__init__(catr_api,aten_api,bu)
        self.bu_list=bu
        self.CATR_sum=self.hourSum(self.catr)
        self.Aten5G_sum=self.hourSum(self.aten_5G)
        self.Aten4G_sum=self.hourSum(self.aten_4G)
        self.BU=self.buSum(self.catr,self.aten_5G,self.aten_4G,bu)

    def hourSum(self,chamber): #計算用了幾小時
        sum=0
        for i in chamber:
            sum+=i['Hours']
        return int(sum)

    def buSum(self,catr,aten5G,aten4G,bu):#計算各bg中的bu分別使用了多少時數
        aten4G_list={}
        aten5G_list={}
        catr_list={}
        for i in bu:
            sum_4G=0; sum_5G=0; sum_catr=0
            for j in catr:
                if j['BU']==i:
                    sum_catr+=j['Hours']
            for j in aten5G:
                if j['BU']==i:
                    sum_5G+=j['Hours']
            for j in aten4G:
                if j['BU']==i:
                    sum_4G+=j['Hours']
            aten4G_list[i]=sum_4G
            aten5G_list[i]=sum_5G
            catr_list[i]=sum_catr

        return {'4G':aten4G_list,'5G':aten5G_list,'catr':catr_list}
