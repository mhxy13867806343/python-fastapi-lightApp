import redis
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
        key = self.author.id + ':' + str(datetime.now().year) + str(datetime.now().month)
        offset = datetime.now().day-1 if offset is None else offset - 1
        self.r.setbit(key, offset, 1)

    # 查询某天签到情况
    def check_sign(self, day):
        offset = day-1
        key = self.author.id + ':' + str(datetime.now().year) + str(datetime.now().month)
        return True if self.r.getbit(key, offset)==1 else False

    # 签到列表
    def sign_list(self):
        ls=[]
        mdate = datetime.now().strftime('%Y-%m')
        for i in range(calendar.monthrange(datetime.now().year, datetime.now().month)[1]):
            date = mdate + '-' + str(i+1)
            if self.check_sign(i+1):
                ls.append(date)
            print(date + '\t' + ('√' if self.check_sign(i+1) else '-'))
        print(ls,22)

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
    zs.do_sign()
    print('当月签到次数：' + str(zs.get_sign_count()))
    print('连续签到天数：' + str(zs.get_continuous_sign_count()))
    print('aaa:',zs.check_sign(111))
    zs.sign_list()
