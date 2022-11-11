from pydantic import BaseModel
from typing import Optional
class UserToekRet(BaseModel):
    username:Optional[str]=None
