import uvicorn
import logging

from fastapi import FastAPI,Depends,Request,status
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles #静态文件操作
from fastapi.middleware.cors import CORSMiddleware # CORS
from starlette.responses import JSONResponse

from extend.db import LOCSESSION,Base,ENGIN # for database
from apps.user.views import users as user_routerApi # for users
from apps.home.views import home as home_routerApi # for users
from apps.histiry.views import histiry as histiry_routerApi # for users
from apps.dicts.views import dicts as dicts_routerApi # for users
from apps.semail.views import emails as emails_routerApi # for users
from apps.emoji.views import emoji as emoji_routerApi # for users
authorizations = {
    'Basic Auth': {
        'type': 'basic',
        'in': 'header',
        'name': 'Authorization'
    },
}

app = FastAPI(
    title="轻应用",
    description="轻应用 api",
    version="2.0.0.1",
openapi_version="3.0.2",
    authorizations=authorizations,
)
app.include_router(user_routerApi)
app.include_router(home_routerApi)
app.include_router(histiry_routerApi)
app.include_router(dicts_routerApi)
app.include_router(emails_routerApi)
app.include_router(emoji_routerApi)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)

    login_url = str(request.url)[22:]
    #print(login_url,'查看')
    token_url=['dicts/hot','dicts/childList','dicts/childAdd','dicts/add','emoji/list','dicts/list','home/list','histry/upload','users/login','users/register','histry/soupfapig','docs','openapi.json',
               'emails/send']
    user_uploadImg=['.jpg','.png','.gif','.jpeg','webp']
    if (login_url in token_url):  # 屏蔽注册、登录接口, 避免死循环
        return response
    if login_url.find('?')!=-1:
        spilt= login_url.split('?')[0]
        if spilt in token_url:
            return response
    for i in user_uploadImg:
        if login_url.endswith(i):
            return response
    try:
        if (login_url=='users/upload'):
            pass
        token = request.headers['Authorization']  # 获取前端传过来token
        # jwt.decode(token, key=SECRET_KEY)

    except Exception as e:
        logging.warning(e)
        return JSONResponse({'msg': 'token验证失败,请重新登陆!', 'code': status.HTTP_401_UNAUTHORIZED})

    return response
# 静态文件
app.mount('/uploads', StaticFiles(directory='uploads'), name='uploads')
# 创建数据库
Base.metadata.create_all(bind=ENGIN)


if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True, host="localhost", port=8010)