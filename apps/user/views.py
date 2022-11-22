from fastapi import APIRouter, FastAPI, Depends, File, UploadFile, Form, Body
from sqlalchemy.orm import Session
import json
from typing import Union, Optional, List
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from extend.get_db import get_db
from models.user.user_operation import post_user_tag, get_user_tag, user_update_data, get_user_login_by_pwd, \
    post_user_by_zc, get_user_by_id, get_user_by_dynamic, user_update_avter, delete_user_tag, post_user_pwd_update, \
    post_user_login_out
from utils.get_md5_data import get_md5_pwd
from extend.status_code import status_code6011, status_code6006, status_code200, status_code6001, status_code6000, \
    status_code6003, status_code6007, status_code6009
from extend.const_Num import EXPIRE_TIME
from models.user.user_model import User, Dynamic
from models.user.user_ret_model import UserToekRet, UserMyLableRet, UserMyUpPwdRet
from utils import token as createToken  # for token
from extend.redis_db import dbRedis_get,dbRedis_set
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
    content = {"code": 200, "msg": "登录成功", "token": userToken,
               "data": data_user,
               }
    return JSONResponse(content=content)


# 根据用户token去获取用户信息
@users.post('/token', tags=["用户模块"], name="根据token获取用户信息")
def get_user_by_token(id: User = Depends(createToken.pase_token), db: Session = Depends(get_db)):


    user=get_user_by_id(db, id)
    data_user = dbRedis_get(key="user",vname=user.username,name="data")
    if None in data_user:
        return get_user_bys_by_token(db, id)
    else:
        return JSONResponse(content={"code": 200, "msg": "获取成功", "data":eval(data_user[0])})
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
        userSet={
            "data":str(data_user) ,
        }
        dbRedis_set('user',user.username,userSet)
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
async def upload(avatar: Optional[UploadFile] = File(None),
                 db: Session = Depends(get_db),
                 id: User = Depends(createToken.pase_token)
                 ):
    _files = ''
    if avatar:
        _files = 'uploads/users/' + avatar.filename
        rep = await avatar.read()

        with open(_files, 'wb') as f:
            f.write(rep)
    user_update_avter(db, id, _files)
    return {
        "code": 200,
        "msg": "修改成功",
        "data": _files
    }


@users.post("/userSave", tags=["用户模块"], name="用户信息保存")
async def userSave(
        id: User = Depends(createToken.pase_token),
        nickname: Optional[str] = Form(None),
        avatar: Optional[str] = Form(None),
        db: Session = Depends(get_db)):
    user_update_data(db, id, nickname, avatar)
    user = get_user_by_id(db, id)
    data_user = {
        "id": user.id,
        "username": user.username,
        "avatar": user.avatar,
        "reg_time": user.reg_time,
        "nickname": user.nickname,
    }
    return {
        "code": 200,
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
        return {
            "code": status_code200,
            "msg": "修改成功",
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
