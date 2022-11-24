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
class UserPoints(Base):
    __tablename__ = 'user_points'
    id = Column(Integer, primary_key=True,autoincrement=True)
    user_id=Column(Integer,ForeignKey('users.id'))
    user_points=Column(Integer,nullable=False) #当前用户积分
    now_days=Column(Integer,nullable=False,default=0) #当前天数
    is_Check=Column(Integer,nullable=False,default=0) #是否签到 0未签到 1已签到
    check_time=Column(Integer,nullable=False,default=0) #签到时间
    check_In_Days=Column(Integer,nullable=False,default=0) #连续签到天数
    userPoints=relationship('User',backref='user_points')
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
class UserPointsTool(Base):
    __tablename__ = 'user_points_tool'
    id = Column(Integer, primary_key=True,autoincrement=True)
    day=Column(Integer,nullable=False,default=1) #第几天
    lv_points=Column(Integer,nullable=False,default=1) #积分