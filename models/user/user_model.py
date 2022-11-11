from sqlalchemy import Column,Integer,String,ForeignKey

8
from sqlalchemy.orm import relationship
from extend.db import Base,LOCSESSION,ENGIN


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True,autoincrement=True)
    user_number=Column(String(100),nullable=False)
    username = Column(String(255),nullable=False)
    password = Column(String(255),nullable=False)
    avatar = Column(String(255),nullable=False)
    nickname = Column(String(255),nullable=False)
    reg_time = Column(Integer,nullable=False)

class Dynamic(Base):
    __tablename__ = 'dynamic'
    id = Column(Integer, primary_key=True,autoincrement=True)
    username = Column(String(255),nullable=False)
    avatar = Column(String(255), nullable=False)
    content = Column(String(255),nullable=False)
    create_time = Column(Integer,nullable=False)
    dynamic_id=Column(Integer,ForeignKey("users.id"))
    dyname_backref=relationship("User",backref = "stu2class")