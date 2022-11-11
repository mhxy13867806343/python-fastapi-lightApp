import uvicorn
from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware # CORS
from extend.db import LOCSESSION,Base,ENGIN # for database
from apps.user.views import users as user_routerApi # for user
app = FastAPI(
    title="轻应用",
    description="轻应用 api",
    version="1.0.0",
)
app.include_router(user_routerApi)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建数据库
Base.metadata.create_all(bind=ENGIN)


if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True, host="localhost", port=8010)