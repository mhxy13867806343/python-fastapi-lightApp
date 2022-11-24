import redis
from fastapi import FastAPI,Request
import time
from time import mktime
from datetime import date, timedelta,datetime
#
def is_today(target_date):
    print(target_date,int(time.time()))
    import datetime
    aa=datetime.datetime.fromtimestamp(target_date)
    """
    2020-03-25 17:03:55
    Detects if the date is current date
    :param target_date:
    :return: Boolean
    """
    # Get the year, month and day
    c_year = datetime.datetime.now().year
    c_month = datetime.datetime.now().month
    c_day = datetime.datetime.now().day
    # Disassemble the date
    date_list = str(aa).split(' ')[0].split('-')
    date_list1 = str(aa).split(' ')[1].split(':')
    t_year = int(date_list[0])
    t_month = int(date_list[1])
    t_day = int(date_list[2])
    t_hour = int(date_list1[0])
    t_minute = int(date_list1[1])
    t_second = int(date_list1[2])
    final = False
    # Compare years, months and days
    if c_year == t_year and c_month == t_month and c_day == t_day\
            and t_hour<24 and t_minute<60 and t_second<60:
        final = True

    return final
def update_is_checked(aa):
    tomorrow = date.today() + timedelta(days=1)
    tomorrow_zero0 = mktime(tomorrow.timetuple())
    tomorrow_zero1 =mktime(time.strptime(aa, '%Y-%m-%d'))
    p0 = int(tomorrow_zero0)
    p1 = int(tomorrow_zero1)
    tb=False
    if(p0==p1):
        tb=True
    return tb

print(update_is_checked('2022-11-15'))
def create_redis_time(dv=1,days=30):
    tomorrow = date.today() + timedelta(days=days)

    tomorrow_zero = mktime(tomorrow.timetuple())
    p1 = int(tomorrow_zero)


    p = (datetime.now() + timedelta(days=days))

    p2 = int(mktime(p.timetuple()))
    if dv==1:#现在的时间
        return int(time.time())
    if dv==-1: #未来 的时间
        return p2