from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from extend.db import Base,LOCSESSION,ENGIN

class Emoji(Base):
    __tablename__ = 'emoji'
    e_id = Column(Integer, primary_key=True,autoincrement=True)
    e_pid = Column(String(255),nullable=False,default=0)
    e_name = Column(String(255),nullable=False)
    e_url = Column(String(255),nullable=False)