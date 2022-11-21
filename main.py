import uvicorn
from fastapi import FastAPI,Depends,Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles #静态文件操作
from fastapi.middleware.cors import CORSMiddleware # CORS
from extend.db import LOCSESSION,Base,ENGIN # for database
from apps.user.views import users as user_routerApi # for users
from apps.home.views import home as home_routerApi # for users
from apps.histiry.views import histiry as histiry_routerApi # for users
from apps.dicts.views import dicts as dicts_routerApi # for users
from apps.semail.views import emails as emails_routerApi # for users
app = FastAPI(
    title="轻应用",
    description="轻应用 api",
    version="1.0.0",
)
app.include_router(user_routerApi)
app.include_router(home_routerApi)
app.include_router(histiry_routerApi)
app.include_router(dicts_routerApi)
app.include_router(emails_routerApi)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# @app.middleware("http")
# async def db_session_middleware(req: Request, call_next):
#     response = await call_next(req)
#     print("db_session_middleware",dir(req),444)
#     return response
# 静态文件
app.mount('/uploads', StaticFiles(directory='uploads'), name='uploads')
# 创建数据库
Base.metadata.create_all(bind=ENGIN)


if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True, host="localhost", port=8010)