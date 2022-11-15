from pydantic import BaseModel
from typing import Optional
class UserToekRet(BaseModel):
    id:Optional[int]
    username:Optional[str]
    nickname:Optional[str]
    avatar:Optional[str]
    content:Optional[str]
    create_time:Optional[int]
    dynamic_id:Optional[int]
