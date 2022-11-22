import redis
from fastapi import FastAPI,Request
import time
from time import mktime
from datetime import date, timedelta,datetime
#
# tomorrow = date.today() + timedelta(days=1)
# tomorrow_zero = mktime(tomorrow.timetuple())
# p1=int(tomorrow_zero)*1000
p=(datetime.now()+timedelta(seconds=10))
p2=int(mktime(p.timetuple()))*1000
vv='2022-11-22 04:44:07.445702'
vv=vv.split('.')[0]
print(vv,222)
vv2=datetime.strptime(vv, "%Y-%m-%d %H:%M:%S")
print(mktime(vv2.timetuple()),333)