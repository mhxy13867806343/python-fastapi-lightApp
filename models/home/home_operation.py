from sqlalchemy.orm import Session
from models.user.user_model import User,Dynamic
#分页当前第几页current,page_size每页多少条数据
def get_home_list_pagenation(db:Session,current:int=1,page_size:int=20)->[Dynamic]:
    _sum=(current-1)*page_size
    users=db.query(Dynamic).offset(_sum).limit(page_size).all()
    return users

#获取总条数
def get_home_list_total(db:Session)->int:
    total=db.query(Dynamic).count()
    return total