from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from extend.db import Base,LOCSESSION,ENGIN

class Dicts(Base):
    __tablename__ = 'dicts'
    id = Column(Integer, primary_key=True,autoincrement=True)
    keys = Column(String(255),nullable=False)

#根据字典表生成对应字段数据
class DictsDict(Base):
    __tablename__ = 'dicts_dict'
    id = Column(Integer, primary_key=True,autoincrement=True)
    key_value = Column(String(255),nullable=False)
    key_name = Column(String(255),nullable=False)
    key_url = Column(String(255),nullable=False)
    key_args = Column(String(255),nullable=False)
    dict_id = Column(Integer, ForeignKey('dicts.id'), nullable=False)
    dict_backref = relationship("Dicts", backref="dicts2class")
class CrawlerHot(Base):
    __tablename__ = 'new_hot'
    hot_id = Column(Integer, primary_key=True,autoincrement=True)
    hot_cid = Column(String(100),nullable=False,default='')
    hot_time = Column(String(100),nullable=False,default='')
    hot_type=Column(String(100),nullable=False,default='')
    hot_name=Column(String(100),nullable=False,default='')
    hot_count=Column(String(100),nullable=False,default='')
    hot_url=Column(String(255),nullable=False,default='')
    dict_id = Column(Integer, ForeignKey('dicts_dict.id'), nullable=False)
    dict_backref = relationship("DictsDict", backref="hot2class")