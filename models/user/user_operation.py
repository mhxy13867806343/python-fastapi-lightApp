#数据库操作
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import random
import datetime
import time
import uuid
from extend.redis_db import dbRedis_del
from models.user.user_model import UserTagLable,User,Dynamic,MyLable,Signature,UserUpImages,CircleOperation,UserPoints,UserSampleNumId,UserSampleNumIdHot
from extend.dataReturn import intReturn_1, intReturn_2, intReturn_a
from extend.redis_cache import create_redis_time
from utils.signIn import AuthorId,AuthorSign
def create_uuid(name,time,pwd):
    data="{}{}{}".format(name,time,pwd)
    d=uuid.uuid5(uuid.NAMESPACE_DNS, data)
    return d
def create_random_hot(db:Session,num=7):

    try:
        t = random.sample(range(100, 99999), k=num)
        for i in t:
            data = UserSampleNumIdHot(hot_id_num=i)
            db.add(data)
            db.commit()
            db.flush()
    except Exception as e:
        db.rollback()
def create_random_user_num(db:Session):
    try:
        t = random.sample(range(10000, 999999999999999), k=50000)
        for i in t:
            data = UserSampleNumId(n_type_num=i, n_is_delte=0, n_is_usage=0)
            db.add(data)
            db.commit()
            db.flush()
    except Exception as e:
        db.rollback()

def get_samplenumIdhot(db:Session)->list:
    return db.query(UserSampleNumIdHot).all()
#登录用户 -1 用户名不存在 -2 密码错误 users 登录成功
def get_user_login_by_pwd(db:Session,username:str='',pwd:str='')->User:
    userTup = (User.id, User.username, User.avatar, User.nickname, User.reg_time,User.pwdCount,User.pwdTime,
               User.user_type_num
               )
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
    userTup = (User.id, User.username, User.avatar, User.nickname, User.reg_time,User.pwdCount,User.pwdTime,User.user_type_num)
    user = db.query(*userTup).filter(User.id == user_id).first()
    return user
#根据某个用户发动态
def get_user_by_dynamic(db:Session,uid:int,content:str='',positioning:str=''):
    userTup = (User.id, User.username, User.avatar, User.nickname,User.user_type_num)
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
def user_update_data(db:Session,id:int,nickname:str='',avatar:str='',user_num:str=0):
    user=db.query(User).filter(User.id==id).first()
    if nickname:
        user.nickname=nickname
    if avatar:
        user.avatar=avatar
    if user_num==0 or not user_num or user_num=='':
        return intReturn_2
    if user_num:
        user.user_type_num=user_num
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
        userb=db.query(User).filter(User.id == id).update(
            {User.password: password,
             User.pwdCount: user.pwdCount-1,
             User.pwdTime: create_redis_time(-1)
             }
        )
        db.commit()
        db.flush()
        return user
    except Exception as e:
        return ''
#用户添加签名
def post_add_user_signature(db:Session,uid:int,signature:str=''):
    try:
        user=db.query(Signature).join(User).filter(User.id == Signature.user_id).filter(User.id == uid).first()
        if user:
            if(user.create_time>0):
                print('已经添加过签名')
                user=db.query(Signature).filter(User.id == Signature.user_id,Signature.signature!=signature).update(
                    {Signature.signature: signature },synchronize_session=False
                )
                db.commit()
                db.flush()
                return user
        else:
            print('没有添加过签名')
            signature1=Signature(user_id=uid,signature=signature,create_time=int(time.time()))
            db.add(signature1)
            db.commit()
            db.flush()
            return -1
    except Exception as e:
        pass
#获取用户签名
def get_user_signature(db:Session,uid:int):
    try:
        user = db.query(Signature).join(User).filter(User.id==Signature.user_id).filter(User.id==uid).first()
        return user
    except Exception as e:
        pass
#修改用户签名
def post_update_user_signature(db:Session,uid:int):
    try:
        user = db.query(Signature).join(User).filter(User.id==Signature.user_id).filter(User.id==uid).first()
        db.update(user)
        db.commit()
        db.flush()
    except Exception as e:
        pass


#退出登录
def post_user_login_out(db:Session,id:int):
    try:
        user=db.query(User).filter(User.id==id).first()

        if user:
            dbRedis_del(key="user",vname=user.username)
            return user
        return intReturn_1
    except Exception as e:
        return intReturn_1
def post_user_pwd_Count(db:Session,id:int):
    try:
        user = db.query(User).filter(User.id == id).first()

        if user:
            db.query(User).filter(User.id == id).update({
                User.pwdCount:2,
                User.pwdTime:0
            })
            db.commit()
            db.flush()
            return user
        return intReturn_1
    except Exception:
        return intReturn_1


#获取用户上传的图片
def get_user_uploads_my(db:Session,id:int):
    try:
        user=db.query(User).filter(User.id==id).first()
        if user:
            imgList=db.query(UserUpImages).join(User).filter(UserUpImages.p_user_id==user.id).first()
            if imgList:
                return imgList
    except Exception as e:
        print(e)
        return intReturn_1
#保存用户上传图片
def post_user_circleOperation_my(db:Session,uid:int,
                                 c_content:str='',public_type:int=0,c_delete_is:int=0
                                 ):
    print('保存用户上传图片')
    create_time = int(time.time())
    try:
        user=db.query(User).filter(User.id==uid).first()
        dbs = CircleOperation(c_content=c_content,c_user_id=user.id,  c_create_time=create_time
                              , c_delete_is=c_delete_is, c_public_type=public_type,
                              c_name=user.nickname,c_avatar=user.avatar
                              )
        db.add(dbs)
        db.commit()
        db.flush()
        return dbs
    except Exception as e:
        print(e,'aaa')
        return intReturn_1
def post_user_uploads_my(db:Session,uid:int,fileList:list)->list:
    create_time = int(time.time())
    try:
        dbs = UserUpImages(p_user_id=uid, p_images=fileList,p_create_time=create_time)
        db.add(dbs)
        db.commit()
        db.flush()
        return dbs
    except Exception as e:
        return intReturn_1

#分页当前第几页current,page_size每页多少条数据
def get_upyq_list_pagenation(db:Session,current:int=1,page_size:int=20)->[CircleOperation]:
    _sum=(current-1)*page_size
    users=db.query(CircleOperation).filter(CircleOperation.c_delete_is==0).order_by(CircleOperation.c_id.desc()).offset(_sum).limit(page_size).all()
    return users
def get_upyqs_list_pagenation(db:Session)->list:
    users=db.query(UserUpImages).order_by(UserUpImages.p_create_time.desc()).all()
    return users
#获取总条数
def get_upyq_list_total(db:Session)->int:
    total=db.query(CircleOperation).count()
    return total
def get_senum_list_pagenation(db:Session,keys:str='',current:int=1,page_size:int=20)->list:
    _sum = (current - 1) * page_size
    alist=db.query(UserSampleNumId).filter(UserSampleNumId.n_type_num.like("%{}%".format(keys))).offset(_sum).limit(page_size).all()
    return alist
#获取用户id总条数
def get_senum_list_total_uid(db:Session,keys:str='')->int:
    total = db.query(UserSampleNumId).filter(UserSampleNumId.n_type_num.like("%{}%".format(keys))).count()
    return total
#获取用户签到列表
def get_user_sign_list(db:Session,id:int,offset:int=0):
    try:
        user=db.query(User).filter(User.id==id).first()
        author = AuthorId(str(user.id), user.nickname)
        auser = AuthorSign(author)
        if user:
            _dict = {
                "now_days":auser.get_sign_count(),  # 签到第几天了
                "is_Check": 1 if auser.check_sign(offset) else 0,
                "check_In_Days": auser.get_continuous_sign_count(),
            }
            print(_dict, 8888888)
            return _dict
        return intReturn_1
    except Exception as e:
        print(e,'xxxxxxxx')
        return intReturn_1
#设置用户签到
def post_click_user_sign(db:Session,offset:int,uid:int):
    try:
        user = db.query(User).filter(User.id == uid).first()
        if user:
            author = AuthorId(str(user.id), user.nickname)
            auser = AuthorSign(author)
            auser.do_sign(db, user.id, offset)
    except Exception as e:
        return intReturn_1
#获取用户签到天数
def get_user_sign_days(db:Session,id:int):
    try:
        user=db.query(User).filter(User.id==id).first()
        if user:
            point=db.query(func(UserPoints.is_Check==1)).join(User,UserPoints).scalar()
            return point
    except Exception as e:
        return intReturn_1
#获取用户某天是否签到过
def get_user_sign_check(db:Session,uid:int):
    try:
        user = db.query(User).filter(User.id == uid).first()
        if user:
            author = AuthorId(str(user.id), user.nickname)
            auser = AuthorSign(author)
            _sign_list=auser.sign_list()
            return _sign_list
    except Exception as e:
        return intReturn_1
#哪些天未签到的
def post_isUserSampleNumId(db:Session,uid:int,type_num:str='')->bool:
    if not db:
        return -99
    if not uid:
        return -100
    if not type_num:
        return -101
    data=db.query(User).filter(User.id==uid).first()
    if data:
        db.query(UserSampleNumId).filter(UserSampleNumId.n_type_num==type_num).update({
            UserSampleNumId.n_is_usage:1,
            UserSampleNumId.n_user_id:uid,
            UserSampleNumId.n_is_delte:0 })
        db.commit()
        db.flush()
        return data
    return intReturn_1
def get_tagLabel_list(db:Session)->list:
    try:
        data=db.query(UserTagLable).all()
        return data
    except Exception as e:
        return intReturn_1