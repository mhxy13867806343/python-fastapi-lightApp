import redis,time
from datetime import datetime
import calendar

class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class AuthorSignDemo:
    # 创建Redis连接
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)

    def __init__(self, author):
        self.author = author

    # 某天签到
    def do_sign(self, offset=None):
        if offset!=None:
            if offset > datetime.now().day:
                raise ValueError('不能签到未来的日期')
        key = self.author.id + ':' + str(datetime.now().year) + str(datetime.now().month)
        _offset = datetime.now().day-1 if offset is None else offset - 1
        self.r.setbit(key, _offset, 1)
        return offset

    # 查询某天签到情况
    def check_sign(self, day):
        offset = day-1
        key = self.author.id + ':' + str(datetime.now().year) + str(datetime.now().month)
        return True if self.r.getbit(key, offset)==1 else False

    # 签到列表
    def sign_list(self):
        _sign_list=[]
        mdate = datetime.now().strftime('%Y-%m')
        for i in range(calendar.monthrange(datetime.now().year, datetime.now().month)[1]):

            if i + 1 > datetime.now().day-1: #从 每个月1号 开始到今天 -1吧
                # 如果当前日期已经超过今天，则退出循环
                break
            _date = mdate + '-' + str(i + 1)
            _type = 1 if self.check_sign(i + 1) else 0
            vv=_date.split('-')
            a_date = datetime(int(vv[0]), int(vv[1]), int(vv[2]))
            cdo = time.strptime(a_date.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            second = int(time.mktime(cdo))
            #与后端字段相同
            _sign_list.append({
                "now_days": datetime.now().day-1,  #签到第几天了
                "is_Check": _type, #哪天签到过了
                "check_In_Days": self.get_continuous_sign_count(), #连续签到天数
                "user_id": self.author.id, #用户id
                "check_time": second#签到时间戳
            })
        print(_sign_list,22)

    # 签到天数统计
    def get_sign_count(self):
        key = self.author.id + ':' + str(datetime.now().year) + str(datetime.now().month)
        return self.r.bitcount(key)

    # 连续签到天数
    def get_continuous_sign_count(self):
        key = author.id + ':' + str(datetime.now().year) + str(datetime.now().month)
        continues_count = 0
        res = 0
        for i in range(calendar.monthrange(datetime.now().year, datetime.now().month)[1]):
            if i + 1 > datetime.now().day:
                # 如果当前日期已经超过今天，则退出循环
                break
            if(self.check_sign(i+1)):
                continues_count += 1
                if(continues_count>res):
                    res = continues_count
            else:
                continues_count = 0
        return res

# 测试
if __name__ == '__main__':
    author = Author('10000', '张三')
    zs = AuthorSignDemo(author)
    print('用户ID：' + author.id)
    print('用户姓名：' + author.name)

    zs.do_sign(1)
    zs.do_sign(2)
    zs.do_sign(3)
    zs.do_sign(4)
    print('当月签到次数：' + str(zs.get_sign_count()))
    print('连续签到天数：' + str(zs.get_continuous_sign_count()))
    print('aaa:',zs.check_sign(111))
    zs.sign_list()
