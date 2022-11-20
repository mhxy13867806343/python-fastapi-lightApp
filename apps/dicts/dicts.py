from fastapi import APIRouter, FastAPI, Depends, File, UploadFile, Form
from starlette.responses import JSONResponse
from typing import Union,Optional,List
from extend.status_code import status_code6010,status_code6006,status_code200,status_code6001,status_code6000,status_code6003,status_code6007,status_code6009
from models.dicts.dicts_operation import add_dict,get_dict_list,get_dict_list_total
dicts = APIRouter(
    prefix="/dicts",
    tags=["字典管理"]
)


@dicts.get("/list",name="字典列表")
async def get_dict_lists(key:str='',current:int=1,page_size=20)->list:
    data=get_dict_list(key=key,current=current,page_size=page_size)
    print(data,3333)
    return {
        "code":status_code200,
        "data":data,
        "msg":"查询成功",
        "total":get_dict_list_total()
    }


@dicts.post("/add",name="添加字典")
async def upload(keys:str=Form(...)):
    dicts = add_dict(keys)
    if(dicts=="" or dicts is None):
        return {
            "code":status_code6010,
            "msg":"字典已存在"
        }
    return {
        "code": status_code200,
        "msg":"添加成功",
        "data": keys,
    }