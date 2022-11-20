from fastapi import APIRouter, FastAPI, Depends, File, UploadFile, Form
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from typing import Union,Optional,List
from extend.status_code import status_code6010,status_code6006,status_code200,status_code6001,status_code6000,status_code6003,status_code6007,status_code6009
from extend.get_db import get_db
from models.dicts.dicts_operation import add_child_dict, add_dict,get_dict_list,get_dict_list_total
from models.dicts.dicts_ret_model import DictsRet,DistListRet
dicts = APIRouter(
    prefix="/dicts",
    tags=["字典管理"]
)


@dicts.get("/list",name="字典列表")
async def get_dict_lists(keys:str='',current:int=1,page_size:int=20,db:Session=Depends(get_db)):
    data=get_dict_list(db,keys,current,page_size)
    total=get_dict_list_total(db,keys=keys)
    return {
        "code":status_code200,
        "data":data,
        "msg":"查询成功",
        "total":total
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
# ,
@dicts.post("/childAdd",name="根据父字典添加子字典")
async def childAdd(dict:List[DistListRet],pid:int):
    try:
        for index, item in enumerate(dict):
            data1=add_child_dict(item.key_value, item.key_name,pid)
            if data1==-1:
                return {
                    "code":status_code6006,
                    "msg":"父字典id不存在"
                }
    except Exception as e:
        print(e,4444)
        return {
            "code":status_code6006,
            "msg":"添加失败"
        }
    return {
        "code": status_code200,
        "msg":"添加成功",
    }
    # dicts = add_child_dict(value,name,pid)
    # if(dicts=="" or dicts is None):
    #     return {
    #         "code":status_code6010,
    #         "msg":"字典已存在"
    #     }
    # return {
    #     "code": status_code200,
    #     "msg":"添加成功",
    #     "data": keys,
    # }