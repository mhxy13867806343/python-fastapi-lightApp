import redis
from extend.const_Num import EXPIRE_TIME
rdecodeResponses=redis.Redis(host='localhost',port=6379,decode_responses=True,charset='UTF-8',encoding='UTF-8')

EXPIRE_TIME60=EXPIRE_TIME*1000
#设置
def dbRedis_set(key1='user',vname="vname",data='user',ex=EXPIRE_TIME60):
    rdecodeResponses.set(name=key1+vname,value=data,ex=ex)
#获取
def dbRedis_get(key='user',vname="vname"):
    redis_data=rdecodeResponses.get(key+vname)
    if redis_data is None:
        return ""
    return redis_data
#删除
def dbRedis_del(key='user',vname="vname"):
    rdecodeResponses.delete(key+vname)
def dbRedis_update(key:str='user',data:dict={}):
    rdecodeResponses.hmset(key,data)
def dbRedis_hkeys(key:str='user'):
    return rdecodeResponses.hkeys(key)

def dbRedis_hvals(key:str='user'):
    return rdecodeResponses.hvals(key)