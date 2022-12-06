import redis
import time
from sqlalchemy.orm import Session
import datetime
from datetime import datetime
import calendar


from models.user.user_model import User,UserPoints
from extend.dataReturn import intReturn_1,intReturn_2
def postSign(db:Session,id:int):

    data = db.query(UserPoints).join(User, UserPoints.user_id == id).all()
    print(data[0].is_Check,22222)
    return
    if data is None:
        return 0
    return data.is_Check

class AuthorId:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class AuthorSign:
    # 创建Redis连接
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True,db=15)
    r = redis.Redis(connection_pool=pool)

    def __init__(self, author):
        self.author = author
    #设置过期时间
    def set_expire(self):
        # 获取当前时间
        print('设置过期时间',444444444)
        now = datetime.datetime.now()
        zeroToday = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                             microseconds=now.microsecond)
        # 获取23:59:59
        lastToday = zeroToday + datetime.timedelta(hours=23, minutes=59, seconds=59)
        v4=lastToday.strftime("%H:%M:%S")
        v5 = time.strftime("%H:%M:%S", time.localtime())
        print(v4,v5,'aaaaaaa')
        if(v4!=v5):
            self.r.expire(f"exp-{self.author.id}", 1)
        else:
            self.r.expire(f"exp-{self.author.id}", 0)
        print('添加成功',self.r.get(f"exp-{self.author.id}"))
    #获取过期时间
    def get_expire(self):
        authorNone=self.r.get(f"exp-{self.author.id}")
        print(authorNone,3333333333333333)
        if authorNone is None:
            return intReturn_1
        print('进行中',authorNone)
    # 某天签到
    def do_sign(self,db:Session,id:int, offset=None):
        print('进行中',id,self.check_sign(offset),offset,22222,33333)
        if self.check_sign(offset)==False:

            key = self.author.id + ':' + str(datetime.now().year) + str(datetime.now().month)
            offset = datetime.now().day-1 if offset is None else offset - 1
            self.r.setbit(key, offset, 1)
            check_time = int(time.time())
            is_Check = 1 if offset else 0
            datas = UserPoints(
                user_id=self.author.id,
                is_Check=is_Check, check_time=check_time,
                check_In_Days=self.get_continuous_sign_count(self.author),
                now_days=self.get_sign_count()
            )

            db.add(datas)
            db.commit()
            print('签到成功')
            return datas
        else:
            return intReturn_1

    # 查询某天签到情况
    def check_sign(self, day):
        offset = day-1
        key = self.author.id + ':' + str(datetime.now().year) + str(datetime.now().month)
        return True if self.r.getbit(key, offset)==1 else False

    # 签到列表
    def sign_list(self):
        mdate = datetime.now().strftime('%Y-%m')
        for i in range(calendar.monthrange(datetime.now().year, datetime.now().month)[1]):
            date = mdate + '-' + str(i+1)
            print(date + '\t' + ('√' if self.check_sign(i+1) else '-'))

    # 签到天数统计
    def get_sign_count(self):
        key = self.author.id + ':' + str(datetime.now().year) + str(datetime.now().month)
        return self.r.bitcount(key)

    # 连续签到天数
    def get_continuous_sign_count(self,author):
        key = author.id + ':' + str(datetime.now().year) + str(datetime.now().month)
        continues_count = 0
        res = 0
        for i in range(calendar.monthrange(datetime.now().year, datetime.now().month)[1]):
            if(self.check_sign(i+1)):
                continues_count += 1
                if(continues_count>res):
                    res = continues_count
            else:
                continues_count = 0
        return res
