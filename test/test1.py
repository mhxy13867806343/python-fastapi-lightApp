import redis
import time
import datetime
import schedule
# 获取当前时间
now = datetime.datetime.now()
# 获取今天零点
zeroToday = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
# 获取23:59:59
lastToday = zeroToday + datetime.timedelta(hours=23, minutes=59, seconds=59)

# a=time.mktime(lastToday.strftime( "%Y-%m-%d %H:%M:%S"))

timeArray = time.strptime(lastToday.strftime("%Y-%m-%d %H%M%S"), "%Y-%m-%d %H%M%S")
#转换为时间戳
a = time.mktime(timeArray)

cc=int(a)- int(time.time())
dates = datetime.datetime.strptime(now.strftime('%Y-%m-%d'), '%Y-%m-%d')
start_time = datetime.datetime.combine(dates, datetime.time.min)
end_time = datetime.datetime.combine(dates, datetime.time.max)
aaaa=time.mktime(time.strptime(start_time.strftime("%Y-%m-%d %H%M%S"), "%Y-%m-%d %H%M%S"))
bbbb=time.mktime(time.strptime(end_time.strftime("%Y-%m-%d %H%M%S"), "%Y-%m-%d %H%M%S"))
print(int(aaaa)>-100 ,bbbb,77)
pool = redis.ConnectionPool(host='localhost', port=6379, db=15)
r = redis.StrictRedis(connection_pool=pool)
# r.set(name='key', value='value',ex=cc)
# def main():
#     if (r.get('key')):
#         print('离今天签到还有:',cc,'秒')
#     else:
#         print('结束',cc)
#         r.set(name='key', value='value',ex=cc)
#         return
# schedule.every(1).seconds.do(main)
# while cc>=0:
#     schedule.run_pending()
#     time.sleep(1)
#     cc-=1