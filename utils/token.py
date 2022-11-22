#密码加密
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime import datetime,timedelta
pwd_context=CryptContext(schemes=['bcrypt'], deprecated='auto')



SECRET_KEY="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7" #自定义的
ALGORITHM= "HS256"

oauth_scheme= OAuth2PasswordBearer(tokenUrl="login")

def get_hash_pwd(password:str):
    return pwd_context.hash(password)


#生成token用户信息，过期时间
def create_token(data:dict,expires_delta):
    if expires_delta:
        expire=datetime.utcnow()+expires_delta
    else:
        expire=datetime.utcnow()+timedelta(minutes=30)
    data.update({"exp":expire})
    token= jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token
#解构token
def pase_token(token:str=Depends(oauth_scheme)):
    token_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                  detail={
                        "code": status.HTTP_401_UNAUTHORIZED,
                        "msg": "用户信息已过期或者token错误",
                  },
                    headers={"WWW-Authenticate": "Bearer"}
                  )
    try:
        jwk_data = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id = jwk_data.get("sub")
        if id is None or id == "":
            raise token_exception
    except JWTError as e:
        raise token_exception

    return id







