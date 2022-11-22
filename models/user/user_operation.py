#数据库操作
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import time
import uuid
from extend.redis_db import dbRedis_del
from models.user.user_model import User,Dynamic,MyLable
from extend.dataReturn import intReturn_1,intReturn_2

def create_uuid(name,time,pwd):
    data="{}{}{}".format(name,time,pwd)
    d=uuid.uuid5(uuid.NAMESPACE_DNS, data)
    return d

#登录用户 -1 用户名不存在 -2 密码错误 users 登录成功
def get_user_login_by_pwd(db:Session,username:str='',pwd:str='')->User:
    userTup = (User.id, User.username, User.avatar, User.nickname, User.reg_time,User.pwdCount,User.pwdTime)
    _username= db.query(*userTup).filter(User.username==username).first()
    if _username is None or _username=='':
        return intReturn_1
    user=db.query(*userTup).filter(User.username==username,User.password==pwd).first()
    return user if user else -2

#注册用户
def post_user_by_zc(db:Session,username:str,password:str):
    user=db.query(User).filter(User.username==username).first()
    if user is None:
        reg_time=int(time.time())
        user_number=create_uuid(username,reg_time,password)
        user_id=password+str(reg_time)
        user=User(username=username,password=password,reg_time=reg_time,
                  user_id=user_id,
                  user_number=user_number,avatar='',nickname=username
                  )
        db.add(user)
        db.commit()
        db.flush()
        return user
    else:
        return ""

#根据用户id获取用户信息
def get_user_by_id(db:Session,user_id:int):
    userTup = (User.id, User.username, User.avatar, User.nickname, User.reg_time,User.pwdCount,User.pwdTime)
    user = db.query(*userTup).filter(User.id == user_id).first()
    return user
#根据某个用户发动态
def get_user_by_dynamic(db:Session,uid:int,content:str='',positioning:str=''):
    userTup = (User.id, User.username, User.avatar, User.nickname)
    user=db.query(*userTup).filter(User.id==uid).one()
    create_time = int(time.time())
    if user:
        dy=db.query(Dynamic).filter(Dynamic.dynamic_id==uid).all()
        if len(dy)>0:
            last_time=dy[len(dy)-1].create_time
            #20s内不能重复发动态
            if (create_time-last_time)<20:
                return intReturn_1
        dynamic = Dynamic(dynamic_id=uid, content=content, create_time=create_time,
                          avatar=user.avatar, username=user.username,positioning=positioning)
        db.add(dynamic)
        db.commit()
        db.flush()
        db.refresh(dynamic)
        return dynamic
#编辑数据
def user_update_avter(db:Session,id:int,avatar:str=''):
    user=db.query(User).filter(User.id==id).first()
    if avatar:
        user.avatar=avatar
    db.commit()
    db.flush()
    return user
def user_update_data(db:Session,id:int,nickname:str='',avatar:str=''):
    user=db.query(User).filter(User.id==id).first()
    if nickname:
        user.nickname=nickname
    if avatar:
        user.avatar=avatar
    db.commit()
    db.flush()
    return user
#获取用户标签
def get_user_tag(db:Session,id:int)->list:
    user=db.query(User).filter(User.id==id).first()
    if user:
        label = db.query(MyLable).join(User,MyLable.lable_id==user.id).order_by(MyLable.reg_time.desc()).all()
        return label
#添加用户标签
def post_user_tag(db:Session,uid:int,label:str)->list:
    user=db.query(User).filter(User.id==uid).first()
    if user:
        create_time = int(time.time())
        mylabel=MyLable(lable_id=uid,lable_name=label,reg_time=create_time,is_delete=0)
        db.add(mylabel)
        db.commit()
        db.flush()
        return mylabel
    else:
        return []
#删除用户标签
def delete_user_tag(db:Session,uid:int,id:int):
    _uid=db.query(User).filter(User.id==uid).first()
    if _uid:
        user, label = db.query(User, MyLable).join(User, MyLable.id == id).first()
        if user:
            db.delete(label)
            db.commit()
            db.flush()
            return label

''

#修改密码
def post_user_pwd_update(db:Session,id:int,password:str):
    try:
        user=db.query(User).filter(User.id==id).first()
        if user.password==password:
            return intReturn_1
        if user.pwdCount==0:
            return intReturn_2
        user=db.query(User).filter(User.id == id).update(
            {User.password: password,
             User.pwdCount: user.pwdCount-1,
             User.pwdTime: int(time.time())
             }
        )
        db.commit()
        db.flush()
        return user
    except Exception as e:
        return ''
#退出登录
def post_user_login_out(db:Session,id:int):
    try:
        user=db.query(User).filter(User.id==id).first()

        if user:
            dbRedis_del(key="user",vname=user.username)
            return user
        return intReturn_1
    except Exception as e:
        print(e,444444444)
        return intReturn_1