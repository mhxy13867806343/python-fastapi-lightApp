from sqlalchemy import Column,Integer,String,ForeignKey

8
from sqlalchemy.orm import relationship
from extend.db import Base,LOCSESSION,ENGIN


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True,autoincrement=True)
    user_number=Column(String(100),nullable=False)
    user_id=Column(String(100),nullable=False)
    username = Column(String(255),nullable=False)
    password = Column(String(255),nullable=False)
    pwdCount=Column(Integer,nullable=False,default=2)
    pwdTime=Column(Integer,nullable=False)
    avatar = Column(String(255),nullable=False)
    nickname = Column(String(255),nullable=False)
    reg_time = Column(Integer,nullable=False)

class Signature(Base):
    __tablename__ = 'signature'
    id = Column(Integer, primary_key=True,autoincrement=True)
    user_id=Column(Integer,ForeignKey('users.id'))
    signature=Column(String(255),nullable=False)
    signature_backref = relationship("User", backref="signature2class")
    create_time=Column(Integer,nullable=False)
class Dynamic(Base):
    __tablename__ = 'dynamic'
    id = Column(Integer, primary_key=True,autoincrement=True)
    username = Column(String(255),nullable=False)
    avatar = Column(String(255), nullable=False)
    content = Column(String(255),nullable=False)
    create_time = Column(Integer,nullable=False)
    dynamic_id=Column(Integer,ForeignKey("users.id"))
    dyname_backref=relationship("User",backref = "stu2class")
    positioning = Column(String(255), nullable=False)
class MyLable(Base):
    __tablename__ = 'mylable'
    id = Column(Integer, primary_key=True,autoincrement=True)
    lable_name = Column(String(255),nullable=False)
    lable_id=Column(Integer,ForeignKey("users.id"))
    lable_backref=relationship("User",backref = "label2class")
    #0 未删除 1 已删除
    is_delete = Column(Integer, nullable=False,default=0)
    reg_time = Column(Integer, nullable=False)