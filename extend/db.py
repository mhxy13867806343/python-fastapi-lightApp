from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from sqlalchemy.ext.declarative import declarative_base

username="root" # 数据库用户名
password="123456" # 数据库密码
host="localhost" # 数据库地址
port=3306 # 数据库端口
db_name="lightApp" # 数据库名

url=f"mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}?charset=utf8"

ENGIN=create_engine(url,echo=True)

LOCSESSION=sessionmaker(bind=ENGIN)
# 从sqlalchemy中创建基类
Base=declarative_base()