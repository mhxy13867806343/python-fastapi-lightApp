from sqlalchemy.orm import Session
from sqlalchemy import and_, or_,exists,not_

from extend.db import LOCSESSION,Base,ENGIN # for database
from models.dicts.dicts_model import Dicts,DictsDict,CrawlerHot
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
def add_child_dict(value:str,name:str,url:str,key_args:str,pid:int)->list:
    dicts = session.query(Dicts).filter(Dicts.id==pid).first()
    if dicts:
        dicts = DictsDict(key_value=value, key_name=name, dict_id=pid,key_url=url,key_args=key_args)
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
def get_dict_hot_list(db:Session,type:str='all',current:int=1,page_size:int=20)->[CrawlerHot]:
    _sum = (current - 1) * page_size
    if type=='' or type=='all':

        dicts = db.query(CrawlerHot).offset(_sum).limit(page_size).all()
        return dicts
    all_Dict = db.query(CrawlerHot).filter(CrawlerHot.hot_type==type).order_by(CrawlerHot.hot_time.desc()).offset(_sum).limit(page_size).all()
    return all_Dict
def get_dict_hot_list_total(db:Session,type:str='all')->int:
    if type=='' or type=='all':
        total = db.query(CrawlerHot).count()
        return total
    total = db.query(CrawlerHot).filter(CrawlerHot.hot_type==type).count()
    return total