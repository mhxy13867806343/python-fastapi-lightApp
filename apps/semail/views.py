from fastapi import APIRouter, FastAPI, Depends, File, UploadFile, Form
from sqlalchemy.orm import Session
from extend.status_code import status_code6010,status_code6006,status_code200,status_code6001,status_code6000,status_code6003,status_code6007,status_code6009
from models.semail.semail_operation import send_email as send_email_db
emails = APIRouter(
    prefix="/emails",
    tags=["邮件管理"]
)
@emails.post("/send",name="邮件发送")
async def send_email(address:str='',host:str='@qq.com',cotent:str='test',subject:str='测试邮件'):
    em=send_email_db(address,host,cotent,subject)
    return {
        "code": status_code200,
        "msg":"发送成功",
        "data": em
    }