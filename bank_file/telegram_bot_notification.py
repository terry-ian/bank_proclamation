#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pymysql
import time
import telegram
import pandas as pd
import datetime
from pandas import DataFrame
import telepot
from telepot.loop import MessageLoop
#-340019778   -364811652


# In[17]:


#while True:
#资料库 连线设定
db = pymysql.Connect(host="remotemysql.com",user="giaX9JoXo3",passwd="VEm7Ky6FIB",port=3306,database="giaX9JoXo3",charset = 'utf8')
#查詢目前數據庫中有無訊息要更新
sql_select = "select * from notification_bank where status=0"
df = pd.read_sql(sql_select, con=db)

#目前有多少数据未完成传送
tasknumber=len(df)

if tasknumber == 0 :
    time.sleep(5)
else :
    for i in range(tasknumber): 
        #传送至 telegram 群内
        bot = telepot.Bot(token='1020859504:AAEb-tLbaBjJvJqBsLCzCsStrgTlZNqXRR8')
        value1=df.iloc[i, 3]
        value2=df.iloc[i, 4]
        value3=df.iloc[i, 5]
        value4=df.iloc[i, 6] #(datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')  #时间加8小时 +datetime.timedelta(hours=8)
        bot.sendMessage(chat_id='-364811652',text= '[银行名称] : '+value1+ "\n" +'[标题公告] : '+ value2 + "\n" +'[重要讯息] : '+value3+ "\n"+'[讯息网址] : ' +value4)

        my_cousor = db.cursor()   
        my_cousor.execute( "UPDATE notification_bank SET status = 1  WHERE id = " + str(df.iloc[i, 0]) )
        db.commit()
        my_cousor.close() #关闭游标

db.close()    #关闭连接


# In[ ]:




