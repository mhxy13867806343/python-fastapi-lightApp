from pydantic import BaseModel
from typing import Optional
class  EmojiRet(BaseModel):
    e_name:Optional[str]=''
    e_url:Optional[str]=''