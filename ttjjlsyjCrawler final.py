# -*- coding: utf-8 -*-
import requests
import time
from bs4 import BeautifulSoup
import random
import pandas
import numpy

#对于用run_detail1解析的soup，用soup.find_all(class_='ui-font-middle ui-color-red ui-num')也能返回一些tag，这些tag是基金的当日涨幅（绝对值+百分比）。没啥用。

def geturl_gbk(url):
    html=requests.get(url,headers=header).content.decode('gbk')
#    lxml是一种解析器，接卸html文件。解析后，实际上是得到了一个html格式的字符串。
    soup=BeautifulSoup(html,'lxml')
    return soup

def geturl_utf8(url):
    html=requests.get(url,headers=header).content.decode('utf-8')
    soup=BeautifulSoup(html,'lxml')
    return soup	

#这种格式的网址样例：000009，货币基金？多了年化收益项
def run_detail2(code, name, soup):
    tags=soup.select('dd')
    try:
#        tag.string是在相邻两个尖括号之间的内容
#        tags[1].find_all('span')[0].string是7日年化
#        tags[2].find_all('span')[0].string是14日年化
#        tags[3].find_all('span')[0].string是28日年化
        d1 = tags[0].find_all('span')[0].string
        m1 = tags[4].find_all('span')[1].string
        y1 = tags[5].find_all('span')[1].string
        m3 = tags[6].find_all('span')[1].string
        y3 = tags[7].find_all('span')[1].string
        m6 = tags[8].find_all('span')[1].string
        rece = tags[9].find_all('span')[1].string   
        dfFdDat1 = pandas.DataFrame(columns = ['代码', '名称', '当前', '近1月','近3月','近6月','近1年','近3年','成立来'],index=['0'])
        dfFdDat1['代码'][0] = code
        dfFdDat1['名称'][0] = name
        dfFdDat1['当前'][0] = d1
        dfFdDat1['近1月'][0] = m1
        dfFdDat1['近3月'][0] = m3
        dfFdDat1['近6月'][0] = m6
        dfFdDat1['近1年'][0] = y1
        dfFdDat1['近3年'][0] = y3
        dfFdDat1['成立来'][0] = rece        
        return dfFdDat1   
    except:
        dfFdDat1 = pandas.DataFrame(columns = ['代码', '名称', '当前', '近1月','近3月','近6月','近1年','近3年','成立来'],index=['0'])
#        即使无法读取数据，也要返回代码和名称，以便于debug
        dfFdDat1['代码'][0] = code
        dfFdDat1['名称'][0] = name
        return dfFdDat1

#这种格式的网址样例：000001，非货币基金？
def run_detail1(code, name, soup):
    tags=soup.select('dd')
    try:
#        tags[0].find_all('span')[0].string是当日净值估算
#        tags[0].find_all('span')[1].string是当日净值增长额
#        tags[0].find_all('span')[2].string是当日净值增长百分比
#        tags[3].find_all('span')[0].string是前一日净值
#        tags[3].find_all('span')[1].string是前一日净值增长百分比
#        tags[6].find_all('span')[0].string是累计净值
        d1 = tags[0].find_all('span')[0].string
        m1 = tags[1].find_all('span')[1].string
        y1 = tags[2].find_all('span')[1].string
        m3 = tags[4].find_all('span')[1].string
        y3 = tags[5].find_all('span')[1].string
        m6 = tags[7].find_all('span')[1].string
        rece = tags[8].find_all('span')[1].string   
        dfFdDat1 = pandas.DataFrame(columns = ['代码', '名称', '当前', '近1月','近3月','近6月','近1年','近3年','成立来'],index=['0'])
        dfFdDat1['代码'][0] = code
        dfFdDat1['名称'][0] = name
        dfFdDat1['当前'][0] = d1
        dfFdDat1['近1月'][0] = m1
        dfFdDat1['近3月'][0] = m3
        dfFdDat1['近6月'][0] = m6
        dfFdDat1['近1年'][0] = y1
        dfFdDat1['近3年'][0] = y3
        dfFdDat1['成立来'][0] = rece        
        return dfFdDat1
    except:
        run_detail2(code,name,url)

#UA_LIST是浏览器内核？
UA_LIST = [ "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24" ]
#header是html的选项
header={ 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate, sdch', 'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6', 'Connection': 'keep-alive','User-Agent': random.choice(UA_LIST) }
dfFdDat = pandas.DataFrame(columns = ['代码', '名称', '当前', '近1月','近3月','近6月','近1年','近3年','成立来'])
fIn = '基金名称列表.csv'
dfFundInfo = pandas.read_csv(fIn,encoding='utf_8_sig',engine='python',dtype=object)
ICount = 0
for FundId in dfFundInfo.iloc[:,0]:
    ICount += 1
    code = FundId
    name = dfFundInfo['2'][dfFundInfo.iloc[:,0]==FundId].iloc[0]
#    这个网站还有之前11天的净值数据，但感觉用处不大。
#    更多的净值信息信息在http://fundf10.eastmoney.com/jjjz_000003.html之类的网站，但是信息不是显式存储的，太麻烦了。
    url = 'http://fund.eastmoney.com/' + FundId + '.html'
    time.sleep(numpy.random.rand(1))
    while True:
        try:
            soup1 = geturl_utf8(url)
            dfFdDat1 = run_detail1(code, name, soup1)
            break
        except:
            try:
                soup1 = geturl_utf8(url)
                dfFdDat1 = run_detail2(code, name, soup1)
                break
            except:
                time.sleep(numpy.random.rand(1)*60)
                continue
    dfFdDat = dfFdDat.append(dfFdDat1)
#    每1000行数据输出到文件一次，重置数据表
    if ICount%1000 == 0:
        fOut = '基金历史业绩列表'+str(ICount-999)+'-'+str(ICount)+'.csv'
        dfFdDat.to_csv(fOut,index=False,header=True,encoding='utf_8_sig')
        dfFdDat = pandas.DataFrame(columns = ['代码', '名称', '当前', '近1月','近3月','近6月','近1年','近3年','成立来'])
fOut = '基金历史业绩列表'+str(int(ICount/1000)*1000+1)+'-'+str(ICount)+'.csv'
dfFdDat.to_csv(fOut,index=False,header=True,encoding='utf_8_sig')