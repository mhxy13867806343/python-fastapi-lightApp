from fastapi import APIRouter, FastAPI, Depends, File, UploadFile, Form
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from extend.get_db import get_db
from models.home.home_operation import get_home_list_pagenation,get_home_list_total
from models.user.user_model import User,Dynamic


home = APIRouter(
    prefix="/home",
    tags=["动态列表管理"]
)


@home.get("/list")
def get_user_info(curren_page: int = 1, page_size: int =20, db: Session = Depends(get_db)):
    data=get_home_list_pagenation(db,curren_page,page_size)
    total = get_home_list_total(db)
    return {
        "code": 200,
        "msg":"获取成功",
        "list":data,
        "total":total,
        "page":curren_page,
        "page_size":page_size
    }
