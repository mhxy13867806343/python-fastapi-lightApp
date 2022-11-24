
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
class UserMySignature(BaseModel):
    user_id:Optional[int]
    signature:Optional[str]=''
class UserPointsRet(BaseModel):
    user_id: Optional[int]
    user_points:Optional[int]=0  # 当前用户积分
    now_days:Optional[int]=0  # 当前天数
    is_Check:Optional[int]=0  # 是否签到 0未签到 1已签到
    check_time:Optional[int]=0 # 签到时间
    check_In_Days:Optional[int]=0 # 连续签到天数
