from fastapi import APIRouter, FastAPI, Depends, File, UploadFile, Form
from starlette.responses import JSONResponse
from typing import Union,Optional,List
import requests
import time
from extend.status_code import status_code6006,status_code200,status_code6001,status_code6000,status_code6003,status_code6007,status_code6009
from extend.const_Num import API_KEY
histiry = APIRouter(
    prefix="/histry",
    tags=["版本管理"]
)


@histiry.get("/list")
async def get_histry():
    histryList=[
        {
            "id": 2,
            "name": "优化",
            "version": "0.0.1-a",
            "time": "2021-03-02",
            "description": [
                {
                    "id": 1,
                    "name": "优化版本更新组件1。"
                },
                {
                    "id": 2,
                    "name": "优化导航按钮2。"
                }
            ]
        },
        {
            "id":1,
            "name":"更新",
            "version":"0.0.1",

            "time":"2021-03-01",
            "description":[
                {
                    "id":1,
                    "name":"新增版本更新组件。"
                },
                {
                    "id": 2,
                    "name": "新增导航按钮。"
                }
            ]
        },
    ]
    return  JSONResponse(content={"code": status_code200, "msg": "获取成功", "list": histryList})


@histiry.post("/upload",name="图片上传")
async def upload(file:Optional[UploadFile]=File(None)):
    _files = 'uploads/histiry/' + file.filename
    rep = await file.read()

    with open(_files, 'wb') as f:
        f.write(rep)
    return {
        "code":200,
        "msg":"上传成功",
        "data":_files
    }
@histiry.get("/soupfapig",name="免费第三方接口")
def add_histry():
    url=f"https://apis.juhe.cn/fapig/soup/query?key={API_KEY}"
    data=requests.get(url)
    print(data.json())
    datas=data.json()
    if(datas['error_code']!=0):
        return {
            "code": datas['error_code'],
            "msg": datas['reason'],
            "data": ""
        }
    return {
        "code":200,
        "msg":"新增成功",
        "data":datas
    }