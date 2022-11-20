from fastapi import APIRouter, FastAPI, Depends, File, UploadFile, Form
from starlette.responses import JSONResponse
from extend.status_code import status_code6006,status_code200,status_code6001,status_code6000,status_code6003,status_code6007,status_code6009

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