import redis
from datetime import datetime
import calendar

class Author:
    def __init__(self, id):
        self.id = id

class AuthorSignDemo:
    # 创建Redis连接
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)

    def __init__(self, author):
        self.author = author

    # 某天签到
    def do_sign(self, offset=None):
        key = str(self.author.id) + ':' + str(datetime.now().year) + str(datetime.now().month)
        offset = datetime.now().day-1 if offset is None else offset - 1
        self.r.setbit(key, offset, 1)
        return self.r

    # 查询某天签到情况
    def check_sign(self, day):
        offset = day-1
        key = str(self.author.id) + ':' + str(datetime.now().year) + str(datetime.now().month)
        return True if self.r.getbit(key, offset)==1 else False

    # 签到列表
    def sign_list(self):
        mdate = datetime.now().strftime('%Y-%m')
        l=[]
        for i in range(calendar.monthrange(datetime.now().year, datetime.now().month)[1]):
            date = mdate + '-' + str(i+1)
            l.append(date + '\t' + ('√' if self.check_sign(i+1) else '-'))
        print(l)
        return l


    # 签到天数统计
    def get_sign_count(self):
        key = str(self.author.id) + ':' + str(datetime.now().year) + str(datetime.now().month)
        return self.r.bitcount(key)

    # 连续签到天数
    def get_continuous_sign_count(self,author):
        key =str( author.id) + ':' + str(datetime.now().year) + str(datetime.now().month)
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
#签到
def clickAuthor(uid,num):
    author = Author(uid)
    zs = AuthorSignDemo(author)
    zs.do_sign(num)
def get_continuous_sign_count(uid):
    author = Author(uid)
    zs = AuthorSignDemo(author)
    return zs.get_continuous_sign_count(author)
def get_sign_count(uid):
    author = Author(uid)
    zs = AuthorSignDemo(author)
    return zs.get_sign_count()

def sign_list(uid):
    author = Author(uid)
    zs = AuthorSignDemo(author)
    return zs.sign_list()