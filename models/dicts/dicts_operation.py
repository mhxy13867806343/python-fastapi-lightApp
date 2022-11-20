
from extend.db import LOCSESSION,Base,ENGIN # for database
from models.dicts.dicts_model import Dicts,DictsDict
session = LOCSESSION()
#添加字典
def add_dict(keys:str):
    dicts = session.query(Dicts).filter(Dicts.keys==keys).first()
    if dicts is None:
        dicts = Dicts(keys=keys)
        session.add(dicts)
        session.commit()
        return dicts
    return ""
#查询字典
def get_dict_list(key:str='',current:int=1,page_size:int=20)->[Dicts]:

    print(len(str(key).replace(' ','')),22222222)
    if key == "":
        _sum = (current - 1) * page_size
        users = session.query(Dicts).offset(_sum).limit(page_size).all()
        print('a````',11)
        return users
    else:
        _sum = (current - 1) * page_size
        users = session.query(Dicts).filter(Dicts.keys.like("%{}%".format(key))).all()
        print('a11111',22)
        return users
#获取总条数
def get_dict_list_total()->int:
    total=session.query(Dicts).count()
    return total