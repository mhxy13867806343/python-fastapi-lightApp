import redis
from fastapi import FastAPI,Request
import time
from time import mktime
from datetime import date, timedelta,datetime
#

def create_redis_time(dv=1):
    tomorrow = date.today() + timedelta(days=30)

    tomorrow_zero = mktime(tomorrow.timetuple())
    p1 = int(tomorrow_zero)

    p = (datetime.now() + timedelta(days=30))

    p2 = int(mktime(p.timetuple()))
    if dv==1:#现在的时间
        return int(time.time())
    if dv==-1: #未来 的时间
        return p2