import datetime
import time


def getYesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    print(yesterday,22222)
    print(yesterday.strftime('%Y-%m-%d %H:%M:%S'))
    timeArray = time.strptime(yesterday.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
    stand = int(time.mktime(timeArray))
    end=int(time.time())
    vv=today.strftime('%Y-%m-%d %H:%M:%S')
    cd=datetime.date.today() - datetime.timedelta(days=1)
    cdo=time.strptime(cd.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
    cd1=time.mktime(cdo)
    print(stand,end,cd1,77)
    return yesterday


# 输出
print(getYesterday())