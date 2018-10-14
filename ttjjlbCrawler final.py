# -*- coding: utf-8 -*-
import requests
#import json
import pandas
import operator
#import numpy
#from datetime import datetime, timedelta

#js返回的数据
rjs = requests.get('http://fund.eastmoney.com/js/fundcode_search.js')
#有用数据的起始位置和结束位置
lloc = (rjs.text).find('[')
rloc = (rjs.text).rfind(']')
#截取有用数据
rjsU = (rjs.text)[lloc+1: rloc]
rjsUlen = len(rjsU)
irjsU=0
dfTotal = pandas.DataFrame()
#从左往右解析
while irjsU < rjsUlen:
    if operator.eq(rjsU[irjsU],'['):
        loc_temp1 = rjsU[irjsU+1: ].find(']')
        str_temp1 = rjsU[irjsU+1: irjsU+1+loc_temp1]
        strcell_temp1 = str_temp1.split(',')
        strcell_temp2 = []
        for str_temp2 in strcell_temp1:
            strcell_temp2.append(str_temp2[1:len(str_temp2)-1])
        
        df_temp1 = pandas.DataFrame(strcell_temp2).T
        dfTotal = dfTotal.append(df_temp1)
#        try:
#            dfTotal = dfTotal.append(df_temp1)
#        except:
#            dfTotal = pandas.DataFrame()
#            dfTotal = dfTotal.append(df_temp1) 
        irjsU = irjsU+1+loc_temp1
    else:
        irjsU = irjsU+1
#解析结果写入csv文件
dfTotal.to_csv('基金名称列表.csv',index=False,header=True,encoding='utf_8_sig')
