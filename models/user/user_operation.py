#数据库操作
from sqlalchemy.orm import Session

from fastapi.responses import JSONResponse
import time
import uuid
from models.user.user_model import User,Dynamic


def create_uuid(name,time,pwd):
    data="{}{}{}".format(name,time,pwd)
    d=uuid.uuid5(uuid.NAMESPACE_DNS, data)
    return d

#登录用户 -1 用户名不存在 -2 密码错误 users 登录成功
def get_user_login_by_pwd(db:Session,username:str='',pwd:str='')->User:
    userTup = (User.id, User.username, User.avatar, User.nickname, User.reg_time)
    _username= db.query(*userTup).filter(User.username==username).first()
    if _username is None or _username=='':
        return -1
    user=db.query(*userTup).filter(User.username==username,User.password==pwd).first()
    return user if user else -2

#注册用户
def post_user_by_zc(db:Session,username:str,password:str):
    user=db.query(User).filter(User.username==username).first()
    if user is None:
        reg_time=int(time.time())
        user_number=create_uuid(username,reg_time,password)
        user=User(username=username,password=password,reg_time=reg_time,
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
    userTup = (User.id, User.username, User.avatar, User.nickname, User.reg_time)
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
                return -1
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