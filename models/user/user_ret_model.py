
from pydantic import BaseModel
from typing import Optional
import time
create_time = int(time.time())
class UserToekRet(BaseModel):
    id:Optional[int]
    username:Optional[str]
    nickname:Optional[str]
    avatar:Optional[str]
    content:Optional[str]
    create_time:Optional[int]
    dynamic_id:Optional[int]
class  UserMyLableRet(BaseModel):
    id:Optional[int]
    lable_name:Optional[str]
    reg_time:Optional[int]=create_time

class  UserMyUpPwdRet(BaseModel):
    password:Optional[str]