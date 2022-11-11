from fastapi import APIRouter, FastAPI, Depends, File, UploadFile, Form
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from datetime import datetime,timedelta
from extend.get_db import get_db
from models.user.user_operation import get_user_login_by_pwd,post_user_by_zc,get_user_by_id,get_user_by_dynamic
from utils.get_md5_data import get_md5_pwd
from extend.status_code import status_code200,status_code6001,status_code6000,status_code6003,status_code6007,status_code6009
from extend.const_Num import EXPIRE_TIME
from models.user.user_model import User,Dynamic
from utils import token as createToken # for token

users = APIRouter(
    prefix="/users",
    tags=["用户模块"],
)
@users.post("/register",tags=["用户模块"],name='注册')
def zc(db:Session=Depends(get_db),username:str="",password:str=""):
    md5_pwd=get_md5_pwd(password)
    user=post_user_by_zc(db,username,md5_pwd)
    if not user or user=="":
        return {"code": status_code6001, "msg": "当前用户已存在,请更换用户名"}
    return {
        "code": status_code200,
        "msg": "注册成功",
    }
@users.post('/login',tags=["用户模块"],name="登录")
def post_user_login(data:OAuth2PasswordRequestForm= Depends(),db:Session=Depends(get_db)):
    password=data.password
    username=data.username
    md5_pwd=get_md5_pwd(password)
    user=get_user_login_by_pwd(db,username,md5_pwd)
    if user ==-1:
        content={
            "code": status_code6000,
            "msg": "用户名未注册,请先注册",
        }
        return JSONResponse(content=content)
    if user ==-2:
        content = { "code": status_code6003,
            "msg": "密码错误",}
        return JSONResponse(content=content)
    expires_delta = timedelta(minutes=EXPIRE_TIME)
    userToken = createToken.create_token({"sub": str(user.id)}, expires_delta)
    data_user={
        "id":user.id,
        "username":user.username,
        "avatar":user.avatar,
        "reg_time":user.reg_time,
        "nickname":user.nickname,
    }
    content = {"code": 200, "msg": "登录成功", "token": userToken,
               "data": data_user,
               }
    return JSONResponse(content=content)

#根据用户token去获取用户信息
@users.post('/token',tags=["用户模块"],name="根据token获取用户信息")
def get_user_by_token(id:User = Depends(createToken.pase_token),db:Session=Depends(get_db)):
    user=get_user_by_id(db,id)
    if user:
        data_user={
            "id":user.id,
            "username":user.username,
            "avatar":user.avatar,
            "reg_time":user.reg_time,
            "nickname":user.nickname,
        }
        content = {"code": status_code200, "msg": "获取成功", "data": data_user,}
        return JSONResponse(content=content)
    content = {
        "msg": "用户信息未找到",
        "code": status_code6007,
    }
    return  JSONResponse(content=content)

#根据用户token去获取用户信息，并可以进行数据的添加
@users.post('/sendpublish',tags=["用户模块"],name="根据token获取用户信息并进行数据的添加")
def postSendpublish(id:User = Depends(createToken.pase_token),db:Session=Depends(get_db),content:str=Form(...)):
    user = get_user_by_dynamic(db,id,content)
    print(user,22222)
    if(user==-1):
        return {
            "msg": f"添加数据时间过短",
            "code": status_code6009,
        }
    return {
        "code": status_code200,
        "msg": "发送成功",
    }
