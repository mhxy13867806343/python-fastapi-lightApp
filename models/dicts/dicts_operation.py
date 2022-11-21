from sqlalchemy.orm import Session
from sqlalchemy import and_, or_,exists,not_

from extend.db import LOCSESSION,Base,ENGIN # for database
from models.dicts.dicts_model import Dicts,DictsDict
from models.dicts.dicts_ret_model import DictsRet
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
#根据父字典添加子字典
def add_child_dict(value:str,name:str,pid:int)->list:
    dicts = session.query(Dicts).filter(Dicts.id==pid).first()
    if dicts:
        dicts = DictsDict(key_value=value, key_name=name, dict_id=pid)
        dictsdy=session.query(DictsDict).filter(DictsDict.key_value==value).all()
        for index, item in enumerate(dictsdy):
            if item.key_value==value:
                session.delete(item)
                session.commit()
        session.add(dicts)
        session.commit()
        return dicts
    return -1

#查询字典
def get_dict_list(db:Session,keys:str='',current:int=1,page_size:int=20)->[Dicts]:
    _sum = (current - 1) * page_size
    users = db.query(Dicts).filter(Dicts.keys.like("%{}%".format(keys))).offset(_sum).limit(page_size).all()
    return users
#获取总条数
def get_dict_list_total(db:Session,keys:str='')->int:
    total = db.query(Dicts).filter(Dicts.keys.like("%{}%".format(keys))).count()
    return total
#获取子字典列表
def get_dict_child_list(db:Session,keys:str='')->[DictsDict]:
    all_Dict = db.query(Dicts).filter(Dicts.keys==keys).first()
    if(all_Dict):
        dicts = db.query(DictsDict).filter(DictsDict.dict_id==all_Dict.id).all()
        return dicts
    return []