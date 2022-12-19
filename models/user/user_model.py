from sqlalchemy import Column,Integer,String,ForeignKey,TEXT,Text,BigInteger
from sqlalchemy.sql import func

import time
from sqlalchemy.orm import relationship
from extend.db import Base,LOCSESSION,ENGIN

def current_timestamp():
    return int(time.time())

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
    user_type_num= Column(String(255), nullable=False,default='0')
class UserPoints(Base):
    __tablename__ = 'user_points'
    id = Column(Integer, primary_key=True,autoincrement=True)
    user_id=Column(Integer,ForeignKey('users.id'))
    now_days=Column(Integer,nullable=False,default=0) #签到天数
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
#朋友圈操作
class CircleOperation(Base):
    __tablename__ = 'circle_operation'
    c_id = Column(Integer, primary_key=True,autoincrement=True)
    c_name=Column(String(255),nullable=False)
    c_avatar=Column(String(255),nullable=False)
    c_content = Column(Text,nullable=False,default='')#朋友圈内容
    c_public_type = Column(Integer,nullable=False,default=0) #0 公开 1 私密
    c_user_id=Column(Integer, ForeignKey('users.id'))#谁发的
    c_lable_backref = relationship("User", backref="circle2class")
    c_create_time =Column(BigInteger,nullable=False,default=current_timestamp)#创建时间
    c_images = Column(Text, nullable=False,default='')#图片
    c_delete_is = Column(Integer, nullable=False,default=0) #0 未删除 1 已删除
class UserUpImages(Base):
    __tablename__ = 'user_pyq_uploadImage'
    p_id = Column(Integer, primary_key=True,autoincrement=True)
    p_user_id = Column(Integer, ForeignKey('users.id'))
    p_images=Column(String(255),nullable=False)
    p_create_time=Column(BigInteger,nullable=False,default=current_timestamp)
    p_lable_backref = relationship("User", backref="cuseupload2class")

class UserSampleNumId(Base):
    __tablename__ = 'user_sample_num'
    n_id=Column(Integer, primary_key=True,autoincrement=True)
    n_type_num= Column(BigInteger, nullable=False,default=0) #与用户进行关联的num_id
    n_user_id = Column(Integer, ForeignKey('users.id'))
    n_is_delte=Column(Integer, nullable=False,default=0) #是否被删除 0未删除  1删除
    n_is_usage=Column(Integer, nullable=False,default=0) #是否被使用 0未使用  1使用
    n_lable_backref = relationship("User", backref="UserSampleNumId2class")
class UserSampleNumIdHot(Base):
    __tablename__ = 'user_sample_hot_num'
    hot_id = Column(Integer, primary_key=True, autoincrement=True)
    hot_id_num = Column(BigInteger, nullable=False, default=0)
class UserTagLable(Base):
    __tablename__ = 'user_tag_label'
    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    tag_name = Column(String(255), nullable=False)
    tag_name_count=Column(Integer,nullable=False,default=0)
    tag_name_id= Column(String(255), nullable=False)
    # 0用户  1动态  其他类型后面再加
    tag_name_type= Column(Integer, nullable=False,default=0)
    tag_name_desc= Column(String(255), nullable=False,default='')



