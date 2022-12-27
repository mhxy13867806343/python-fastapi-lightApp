import os
import time
def osFilePathIsdir(_path:str="uploads"):
    year = time.strftime("%Y", time.localtime())
    moment = time.strftime("%m", time.localtime())
    # 年    月      ID      文件
    ps = f"file/{_path}"
    p = os.path.isdir(ps)
    if not p:
        os.makedirs(ps)
    return ps
