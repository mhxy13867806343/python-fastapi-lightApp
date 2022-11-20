from pydantic import BaseModel
from typing import Optional
class  DictsRet(BaseModel):
    keys:Optional[str]
class DistListRet(BaseModel):
    id:Optional[int]
    key_value:Optional[str]
    key_name:Optional[str]