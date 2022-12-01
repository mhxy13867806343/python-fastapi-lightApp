start =1669045330
import time,requests
import datetime,re
import json
from pyquery import PyQuery as pq
print(int(time.time()))
target_date=int(time.time())
aa=datetime.datetime.fromtimestamp(target_date)
print(aa.strftime('%d'))
varc="2022-11-24\t√"
a=['.jpg','.png','.gif','.jpeg','webp']
def bb(cc):
    print(cc)
    for i in a:
        if cc.endswith(i):
            return True
    return False
print(bb('https://www.baidu.com/img/bd_logo1.webp'))
