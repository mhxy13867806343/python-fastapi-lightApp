import os
import time
print(time.strftime("%m", time.localtime()))
vv='../test/20221201/07'
p=os.path.isdir(vv)
if not p:
    os.makedirs(vv)
else:
    print('已经存在')
