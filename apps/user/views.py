from fastapi import APIRouter, FastAPI, Depends, File, UploadFile, Form, Body
from sqlalchemy.orm import Session
import json
from typing import Union, Optional, List
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from extend.get_db import get_db
from models.user.user_operation import get_upyqs_list_pagenation,post_user_tag, get_user_tag, user_update_data, get_user_login_by_pwd, \
    post_user_by_zc, get_user_by_id, get_user_by_dynamic, user_update_avter, delete_user_tag, post_user_pwd_update, \
post_user_login_out,post_user_pwd_Count,post_add_user_signature,get_user_signature,post_user_circleOperation_my,\
    post_user_uploads_my,get_user_uploads_my,get_upyq_list_pagenation,get_upyq_list_total,get_user_sign_list,post_click_user_sign,\
get_user_sign_check,get_user_sign_check_day,get_not_sign

from utils.get_md5_data import get_md5_pwd
from extend.status_code import status_code6011, status_code6006, status_code200, status_code6001, status_code6000, \
    status_code6003, status_code6007, status_code6009
from extend.const_Num import EXPIRE_TIME
from models.user.user_model import User, Dynamic
from models.user.user_ret_model import UserToekRet,UserMyCircleOperationRet, UserMyLableRet, UserMyUpPwdRet,UserMySignature,UserPointsRet,UserMyUpAvatarRet
from utils import token as createToken  # for token
from extend.redis_db import dbRedis_get,dbRedis_set
from extend.redis_cache import create_redis_time
from utils.tools import osFilePathIsdir
users = APIRouter(
    prefix="/users",
    tags=["用户模块"],
)




@users.post("/register", tags=["用户模块"], name='注册')
def zc(db: Session = Depends(get_db), username: str = "", password: str = ""):
    md5_pwd = get_md5_pwd(password)
    user = post_user_by_zc(db, username, md5_pwd)
    if not user or user == "":
        return {"code": status_code6001, "msg": "当前用户已存在,请更换用户名"}
    return {
        "code": status_code200,
        "msg": "注册成功",
    }


@users.post('/login', tags=["用户模块"], name="登录")
def post_user_login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    password = data.password
    username = data.username
    md5_pwd = get_md5_pwd(password)
    user = get_user_login_by_pwd(db, username, md5_pwd)
    if user == -1:
        content = {
            "code": status_code6000,
            "msg": "用户名未注册,请先注册",
        }
        return JSONResponse(content=content)
    if user == -2:
        content = {"code": status_code6003,
                   "msg": "密码错误", }
        return JSONResponse(content=content)
    expires_delta = timedelta(minutes=EXPIRE_TIME)
    userToken = createToken.create_token({"sub": str(user.id)}, expires_delta)
    data_user = {
        "id": user.id,
        "username": user.username,
        "avatar": user.avatar,
        "reg_time": user.reg_time,
        "nickname": user.nickname,
        "pwdCount": user.pwdCount,
        "pwdTime": user.pwdTime,
    }
    dbRedis_set('user', user.username, data=str(data_user))
    content = {"code": 200, "msg": "登录成功", "token": userToken,
               "data": data_user,
               }
    return JSONResponse(content=content)

def jSONRRedisUser(user,type='ext'):
    data_user = {
        "id": user.id,
        "username": user.username,
        "avatar": user.avatar,
        "reg_time": user.reg_time,
        "nickname": user.nickname,
        "pwdCount": user.pwdCount,
        "pwdTime": user.pwdTime,
    }
    if(type=='ext'):
        dbRedis_set('user', user.username, data=str(data_user))
    return JSONResponse(content={"code": 200, "msg": "获取成功", "data": data_user})
def jSONRRedisUserPwdgt(pwdgt):
    data_user = {
        "id": pwdgt.get('id'),
        "username": pwdgt.get('username'),
        "avatar": pwdgt.get('avatar'),
        "reg_time": pwdgt.get('reg_time'),
        "nickname": pwdgt.get('nickname'),
        "pwdCount": pwdgt.get('pwdCount'),
        "pwdTime": pwdgt.get('pwdTime'),
    }
    return JSONResponse(content={"code": 200, "msg": "获取成功", "data": data_user})
# 根据用户token去获取用户信息
@users.post('/token', tags=["用户模块"], name="根据token获取用户信息")
def get_user_by_token(id: User = Depends(createToken.pase_token), db: Session = Depends(get_db)):
    user=get_user_by_id(db, id)
    gt = dbRedis_get(vname=user.username)
    if not gt:
        print('redis中没有数据')
        return jSONRRedisUser(user,'')
    pwdgt = eval(gt)
    pwdTime = pwdgt.get('pwdTime')
    ctime=create_redis_time()
    print('redis中有数据',ctime,pwdTime)
    print('redis中有数据',ctime-pwdTime)
    print('redis中有数据',(ctime-pwdTime)>0)
    if(pwdgt.get('pwdCount')==0):
        print('redis中有数据,密码过期')
        if(ctime-pwdTime)>=0:
            print('redis中有数据,但是密码已经过期')
            post_user_pwd_Count(db, user.id)

            return jSONRRedisUser(user,'ext')
        else:
            print('redis中有数据,密码没有过期1111')
            return jSONRRedisUserPwdgt(pwdgt)
    else:
        print('redis中有数据,密码没有过期2222')
        return jSONRRedisUser(user,'')
def get_user_bys_by_token(db,id):
    user = get_user_by_id(db, id)
    if user:
        data_user = {
            "id": user.id,
            "username": user.username,
            "avatar": user.avatar,
            "reg_time": user.reg_time,
            "nickname": user.nickname,
            "pwdCount": user.pwdCount,
            "pwdTime": user.pwdTime,
        }
        content = {"code": status_code200, "msg": "获取成功", "data": data_user, }
        return JSONResponse(content=content)
    content = {
        "msg": "用户信息未找到",
        "code": status_code6007,
    }
    return JSONResponse(content=content)


# 根据用户token去获取用户信息，并可以进行数据的添加
@users.post('/sendpublish', tags=["用户模块"], name="根据token获取用户信息并进行数据的添加")
def postSendpublish(id: User = Depends(createToken.pase_token), db: Session = Depends(get_db), content: str = Form(...),
                    positioning: Optional[str] = Form('')
                    ):
    if (not id) or (id == ""):
        return {
            "code": status_code6007,
            "msg": "用户信息不正确",
        }
    user = get_user_by_dynamic(db, id, content, positioning)
    if (user == -1):
        return {
            "msg": f"添加数据时间过短",
            "code": status_code6009,
        }
    return {
        "code": status_code200,
        "msg": "发送成功",
    }


@users.post("/upload", tags=["用户模块"], name="上传头像")
async def upload(file: Optional[UploadFile] = File(None),
                 db: Session = Depends(get_db),
                 id: Optional[User] =Depends(createToken.pase_token)
                 ):
    if id!=None or id!="":
        path_dir=osFilePathIsdir()
        _files = f'{path_dir}/{file.filename}'
        rep = await file.read()

        with open(_files, 'wb') as f:
            f.write(rep)
        user_update_avter(db, id, _files)
        return {
            "code": 200,
            "msg": "上传成功",
            "data": _files
        }
#多张图片上传
@users.post("/uploads",name="上传多张图片",tags=["用户模块"])
async def update_item(files: List[UploadFile] = File(None),
                      db: Session = Depends(get_db),
                      id: Optional[User] = Depends(createToken.pase_token)
                      )->list:
    path_dir = osFilePathIsdir('circlese')
    lists = [f"{path_dir}/{i.filename}" for i in files]
    count = 0
    for i in files:
        _files = f'{path_dir}/{i.filename}'
        with open(f'{_files}','wb') as f:
            f.write(await i.read())
        count += 1
    post_user_uploads_my(db, uid=id, fileList=','.join(lists))
    return {
           "code": status_code200,
            "msg": "上传成功",
            "data": lists
            }
@users.get("/pyclist",name="查看所有的朋友圈内容",tags=["用户模块"])
def pycList(db: Session = Depends(get_db),current:int=1,page_size:int=20,id: Optional[User] = Depends(createToken.pase_token)):
    data=get_upyq_list_pagenation(db,current,page_size)
    total=get_upyq_list_total(db)
    aa=get_upyqs_list_pagenation(db)
    if(len(data)):
        for (index, item) in enumerate(data):
            item.c_images = aa[index].p_images
    return {
        "code": status_code200,
        "msg": "获取成功",
        "list": data,
        "total":total
    }
@users.post("/csave",name="保存用户朋友圈内容",tags=["用户模块"])
async def post_user_circleOperation_mys(
                                         sdata:UserMyCircleOperationRet,
                                        id: User = Depends(createToken.pase_token),
                                        db: Session = Depends(get_db)):
    data=post_user_circleOperation_my(db,id,sdata.c_content,sdata.public_type)
    if(data==-1):
        return {
            "code": status_code6006,
            "msg": "保存失败",
            "data":{}
        }
    return {
        "code": status_code200,
        "msg": "提交成功",
    }
@users.get("/uploads",name="获取多张图片",tags=["用户模块"])
async def get_uploads(id: User = Depends(createToken.pase_token), db: Session = Depends(get_db)):
    data=get_user_uploads_my(db,id)
    if(data==-1):{
        "code": status_code6006,
        "msg": "获取失败",
        "data":[]
    }
    return {
        "code": status_code200,
        "msg": "获取成功",
        "data": data.p_images
    }
@users.post("/userSave", tags=["用户模块"], name="用户信息保存")
async def userSave(
        id: User = Depends(createToken.pase_token),
        nickname: Optional[str] = Form(None),
        avatar: Optional[str] = Form(None),
        db: Session = Depends(get_db)):
    user_update_data(db, id, nickname, avatar)
    user = get_user_by_id(db, id)
    if(not user):
        return {
            "code": status_code6007,
            "msg": "修改失败",
        }
    data_user = {
        "id": user.id,
        "username": user.username,
        "avatar": user.avatar,
        "reg_time": user.reg_time,
        "nickname": user.nickname,
    }
    return {
        "code": status_code200,
        "msg": "修改成功",
        "data": data_user,
    }


@users.post("/label", tags=["用户模块"], name="添加用户标签")
async def plabel(

        labeldata: List[UserMyLableRet],
        id: User = Depends(createToken.pase_token),
        db: Session = Depends(get_db)) -> list:
    try:
        for index, item in enumerate(labeldata):
            if not item.id:
                return {
                    "code": status_code6007,
                    "msg": f"第{index + 1}个用户信息不正确",
                }
            if not item.lable_name:
                return {
                    "code": status_code6006,
                    "msg": f"第{index + 1}个标签名称不能为空",
                }
            data = post_user_tag(db, uid=id, label=item.lable_name)

    except ArithmeticError:
        return {
            "code": status_code6006,
            "msg": "添加失败",

        }
    return {
        "code": status_code200,
        "msg": "添加成功",
    }


@users.get("/label", tags=["用户模块"], name="获取用户标签")
def glabel(
        id: User = Depends(createToken.pase_token),
        db: Session = Depends(get_db)) -> list:
    try:
        data = get_user_tag(db, id)
    except ArithmeticError:
        return {
            "code": status_code6006,
            "msg": "获取失败",

        }
    return {
        "code": 200,
        "msg": "获取成功",
        "data": data
    }


@users.post('/updatpwd', tags=["用户模块"], name="修改密码")
def updatpwd(data: UserMyUpPwdRet, id: int = Depends(createToken.pase_token), db: Session = Depends(get_db)):
    md5_pwd = get_md5_pwd(data.password)
    data = post_user_pwd_update(db, id, md5_pwd)

    if data == -1:
        return {
            "code": status_code6011,
            "msg": "修改的密码与原密码一致,请更换新的密码",
        }
    if data:
        data_user = {
            "id": data.id,
            "username": data.username,
            "avatar": data.avatar,
            "reg_time": data.reg_time,
            "nickname": data.nickname,
            "pwdCount": data.pwdCount,
            "pwdTime": data.pwdTime,

        }
        dbRedis_set('user', data.username, data=str(data_user))
        return {
            "code": status_code200,
            "msg": "修改成功",
            "data": data
        }


@users.delete("/label", tags=["用户模块"], name="删除用户标签")
def dlabel(
        id: int = 0,
        user_id: User = Depends(createToken.pase_token),
        db: Session = Depends(get_db)):
    try:
        data = delete_user_tag(db, user_id, id)
        if (not data) or (data == ""):
            return {
                "code": status_code6006,
                "msg": "删除失败",

            }

    except ArithmeticError as e:
        return {
            "code": status_code6006,
            "msg": "删除失败",

        }
    return {
        "code": 200,
        "msg": "删除成功",
    }


@users.post("/logut", tags=["用户模块"], name="退出登录")
def logut(
          user_id: User = Depends(createToken.pase_token),
          db: Session = Depends(get_db)):
    data=post_user_login_out(db, user_id)
    if(data==-1):
        return {
            "code": status_code6006,
            "msg": "退出失败",

        }
    return {
        "code": status_code200,
        "msg": "退出成功",
    }
@users.post("/getsignature", tags=["用户模块"], name="获取用户签名")
def getSignature(user_id: User = Depends(createToken.pase_token), db: Session = Depends(get_db)):
    signature=get_user_signature(db,user_id)
    return {
        "code": status_code200,
        "msg": "获取成功",
        "data": signature
    }
@users.post("/signature", tags=["用户模块"], name="新增用户签名")
def postSignature(data:UserMySignature,user_id: User = Depends(createToken.pase_token), db: Session = Depends(get_db)):
    signature=post_add_user_signature(db,user_id,data.signature)
    if signature==0:
        return {
            "code": status_code6006,
            "msg": "签名内容一致,无法修改",

        }
    if signature==-1:
        return {
            "code": status_code200,
            "msg": "添加成功",
        }
    return {
        "code": status_code200,
        "msg": "修改成功",
    }

#此接口为测试接口暂时不使用
@users.put("/signature", tags=["用户模块"], name="修改用户签名")
def postSignature(data:UserMySignature,user_id: User = Depends(createToken.pase_token), db: Session = Depends(get_db)):
    # signature=post_update_user_signature(db,user_id,data.signature)
    return {
        "code": status_code200,
        "msg": "修改成功",
    }
@users.post("/signin", tags=["用户模块"], name="用户签到")
def postUserSignin(offset:int,user_id: User = Depends(createToken.pase_token), db: Session = Depends(get_db)):
    import datetime
    today = datetime.date.today()
    if offset!=int(today.strftime('%d')):
        return {
            "code": status_code6006,
            "msg": "签到失败,请检查时间",
        }
    data=post_click_user_sign(db,offset,user_id)
    if data==-1:
        return {
            "code": status_code6006,
            "msg": "签到失败",

        }
    return {
        "code": status_code200,
        "msg": "签到成功",

    }
@users.get("/signin", tags=["用户模块"], name="获取用户签到列表")
def getUserSignin(user_id: User = Depends(createToken.pase_token), db: Session = Depends(get_db)):
    list=get_user_sign_list(db,user_id)
    is_check=get_user_sign_check(db,user_id)
    dba=get_user_sign_check_day(db,user_id)
    import datetime
    now = datetime.datetime.now()
    notSign=get_not_sign(db,user_id,now.strftime("%Y-%m-%d"))

    if dba==-1:
        return {
            "code": status_code6006,
            "msg": "获取失败",
            "data":{
            }
        }
    return {
        "code": status_code200,
        "msg": "获取成功",
        "data": {
            "list": notSign,
            "isCheck": is_check,
            **dba,

        }
    }