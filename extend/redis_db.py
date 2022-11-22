import redis
from extend.const_Num import EXPIRE_TIME
rdecodeResponses=redis.Redis(host='192.168.0.103',port=6379,decode_responses=True,charset='UTF-8',encoding='UTF-8')

EXPIRE_TIME60=EXPIRE_TIME*1000
#设置
def dbRedis_set(key='user',vname="vname",data='user',ex=EXPIRE_TIME60):
    _data={**data,**{'ex':ex}}
    rdecodeResponses.hmset(key+vname,_data)
#获取
def dbRedis_get(key='user',vname="vname",name="user"):
    redis_data=rdecodeResponses.hmget(key+vname,name)
    if redis_data is None:
        return ""
    return redis_data
#删除
def dbRedis_del(key='user',vname="vname"):
    rdecodeResponses.delete(key+vname)