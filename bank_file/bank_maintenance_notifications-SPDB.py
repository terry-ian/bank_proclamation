#!/usr/bin/env python
# coding: utf-8

# In[15]:


import requests
from bs4 import BeautifulSoup
import re
import datetime as dt
from datetime import datetime
import pymysql
import pandas as pd
import time
from urllib.parse import unquote
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bank_mysql_function import *    #sql帳密更改
#代理
#from fake_useragent import UserAgent
#ua = UserAgent()
#ua.random

#反爬虫用 模拟使用者
send_headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
 "Connection": "keep-alive",
 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
 "Accept-Language": "zh-CN,zh;q=0.8" }


# In[16]:


def getNewsDetail(notice,domainname,item,bankname):
    result={}
    title=notice[item].find('a').text.split()[0]
    time=notice[item].find('span',{"class": "c_date"}).text.split()[0]
    urllink=notice[item].select("a")[0]["href"]
    
    if urllink.find("pdf") > 0 :
        souparticle = None
    else :
        browser.get(urllink)
        browser.implicitly_wait(100)
        souparticle = BeautifulSoup(browser.page_source, "html.parser")
    try:
        allcontent = " ".join(souparticle.find('div', {"class": "TRS_Editor"}).text.split())
        if len(allcontent)==0 :allcontent="请查询详细内文"  
    except: 
        allcontent ="请查询详细内文"

    result['bank']=bankname
    result['title']=title
    result['time']=time  #.replace("[", "").replace("]", "")
    result['urllink']=unquote(urllink,encoding="utf-8")
    result['allcontent']=allcontent

    return(result)


# In[17]:


chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
chrome_options.add_argument('--headless')                        #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
chrome_options.add_argument('--disable-dev-shm-usage')
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
chrome_options.add_argument("user-agent=" + user_agent)
browser = webdriver.Chrome(options=chrome_options)
#browser.set_page_load_timeout(60)
browser.get('https://www.spdb.com.cn/home/sygg/')  #browser.implicitly_wait(10)
time.sleep(10) 
soup = BeautifulSoup(browser.page_source, "html.parser")
domainname="https://www.spdb.com.cn"
notice=soup.find('div',{"class": "c_news_body common_list"}).findAll('ul')
noticelen = len(notice)

alldata=[]
for i in range(noticelen):
    datanews=getNewsDetail(notice,domainname,i,"浦发银行")
    alldata.append(datanews)
    time.sleep(2)
#关闭捞取数据
browser.close()
browser.quit() 

#存取原始数据
rowdata_db(alldata,noticelen,"浦发银行")
#存取警示数据
notification_db(alldata,noticelen,"浦发银行")


# In[ ]:




