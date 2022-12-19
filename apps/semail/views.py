from fastapi import APIRouter, FastAPI, Depends, File, UploadFile, Form
from sqlalchemy.orm import Session
from captcha.image import ImageCaptcha,random_color
from io import BytesIO
import base64
import string
import random
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
@emails.get("/code",name="验证码生成")
async def generate_code():
    token = string.digits + string.ascii_letters

    cap = random.sample(token, 6)  # 随机字符，固定数量
    token_str = ''.join(cap)  # 拼接字符串
    img = ImageCaptcha()  # 实例化ImageCaptcha类
    # 这是ImageCaptcha自带的初始化内容width=160, height=60, fonts=None, font_sizes=None，可以自己设置

    RGB = (38, 38, 0)  # 字体色
    bgc = (255, 255, 255)  # 背景色
    code = random_color(50, 180)  # 生成随机颜色
    image = img.create_captcha_image(token_str, RGB, bgc)
    img.create_noise_dots(image=image, color=code, width=10, number=10)
    img.create_noise_curve(image=image, color=RGB)
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    data = buffer.getvalue()
    code= 'data:image/png;base64,' + base64.b64encode(data).decode()
    return {
        "code": status_code200,
        "msg":"生成成功",
        "data": {
            "code":token_str,
            "image":code
        }
    }