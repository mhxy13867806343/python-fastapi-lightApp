from fastapi import APIRouter, FastAPI, Depends, File, UploadFile, Form
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from typing import Union,Optional,List
from extend.status_code import status_code6010,status_code6006,status_code200,status_code6001,status_code6000,status_code6003,status_code6007,status_code6009
from extend.get_db import get_db
from models.emoji.emoji_operation import get_emoji_list
from models.emoji.emoji_model import Emoji
emoji = APIRouter(
    prefix="/emoji",
    tags=["表情管理"]
)

@emoji.get("/list",name="表情列表")
async def emojiList(db:Session=Depends(get_db)):
    data=get_emoji_list(db)
    print(data)
    return {
        "code": status_code200,
        "msg":"查询成功",
        "data":data
    }