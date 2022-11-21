#数据库操作
from sqlalchemy.orm import Session
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
import smtplib
from email.mime.multipart import MIMEMultipart


def send_email(address:str='',host:str='@qq.com',cotent:str='test',subject:str='测试邮件'):
    if not address:
        return -1
    if not host:
        return -2
    if not cotent:
        return -3
    msg_from = f'{address}{host}'  # 发送方邮箱
    passwd = 'bqexlactgniebfcc'

    to = ['869710179@qq.com']  # 接受方邮箱

    # MIMEMultipart类可以放任何内容
    msg = MIMEMultipart()
    _content = cotent
    msg.attach(MIMEText(_content, 'plain', 'utf-8'))
    # 设置邮件主题
    msg['Subject'] = subject
    # 发送方信息
    msg['From'] = msg_from
    # 通过SSL方式发送，服务器地址和端口
    s = smtplib.SMTP_SSL("smtp.qq.com", 465)
    # 登录邮箱
    s.login(msg_from, passwd)
    # 开始发送
    s.sendmail(msg_from, to, msg.as_string())
    print("邮件发送成功")
    return 'ok'