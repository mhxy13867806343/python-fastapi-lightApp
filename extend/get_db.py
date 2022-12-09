from .db import LOCSESSION


def get_db():
    try:
        db=LOCSESSION()
        print('数据库连接成功222')
        yield db
    except Exception as e:
        print(e,'错误中...')
        pass
    finally:
        print('关闭数据库')
        db.close()