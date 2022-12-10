import datetime
import time


def getYesterday():
    today = datetime.date.today()
    print(today.day,22)
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
print(getYesterday())

def xxxx():
    import calendar
    from datetime import date

    today = date.today()
    cal = calendar.Calendar()

    # 显示今年的日历
    for month in cal.yeardatescalendar(today.year, 3):
        # 对于每个月，只显示到今天
        for week in month:
            for day, week_day in week:
                if day == today:
                    # 如果已经到了今天，则退出循环
                    break
                print(f"{day:%B %d}".ljust(20), end="")
            print()
