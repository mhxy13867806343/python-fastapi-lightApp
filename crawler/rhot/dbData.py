from sqlalchemy.orm import Session,sessionmaker
from fastapi import APIRouter, FastAPI, Depends, File, UploadFile, Form
import requests
import time
from pyquery import PyQuery as pq
import threading
from extend.db import ENGIN
from models.dicts.dicts_model import CrawlerHot,DictsDict
LOCSESSION=sessionmaker(bind=ENGIN)
def downJuejin(db:Session,type:str='juejin'):
    itemidl=[]
    hrefl=[]
    countl=[]
    titlel=[]
    result = []
    timel=[]
    fields = ( 'name', 'count',"id", 'url','time')
    url='https://tophub.today/n/QaqeEaVe9R'
    headers={
        "cookie":'Hm_lvt_3b1e939f6e789219d8629de8a519eab9=1669206071; Hm_lpvt_3b1e939f6e789219d8629de8a519eab9=1669701107',
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/106.0.0.0",
    }
    res=requests.get(url,headers=headers)
    text=(res.content.decode('utf-8'))
    data = pq(text).find('section.container')
    data=data.find('.ranklist-contianer .rank-body  a.rank-item-container')
    title=data.find('.s-title')
    for item in title:
      titlel.append(item.text)
    tcount=data.find('.s-tie-count')
    for item in tcount:
        countl.append(item.text.split('‧')[0])
        if(item.text.split(' ')[-1].count('-')>0):
            timel.append(item.text.split('‧')[-1])
    for item in data:
        itemidl.append(item.values()[-1])
        href=f'https://tophub.today{item.values()[1]}'
        hrefl.append(href)
    news=list(zip(titlel,countl,itemidl,hrefl,timel))
    for record in news:
        result.append(dict(zip(fields, record)))
    for item in result:
        cursor=db.query(
            CrawlerHot
        ).filter(CrawlerHot.hot_cid == item['id']).first()
        dictsId=db.query(DictsDict).filter(DictsDict.key_value == type).first()
        if cursor is None:
            db.add(CrawlerHot(hot_cid=item['id'],
                              hot_name=item['name'],hot_count=item['count'],hot_url=item['url'],hot_time=item['time'],
                              dict_id=(dictsId and dictsId.id) or (0)
                              ))
            db.commit()
            db.flush()
        else:
            cursor.hot_count=item['count']
            cursor.hot_type='juejin'
            cursor.hot_url=item['url']
            cursor.hot_name=item['name']
            cursor.hot_cid = item['id']
            cursor.dict_id =(dictsId and dictsId.id) or (0)
            db.commit()
            db.flush()

class MyHotThread(threading.Thread):
    def __init__(self,type:str='juejin'):
        super(MyHotThread, self).__init__()
        self.type=type or 'juejin'
    def run(self):
        type=self.type
        _db=LOCSESSION()
        if type=='juejin':
            downJuejin(_db,type)
        elif type=='zhihu':
            pass
        elif type=='baidu':
            pass
        elif type=='weixin':
            pass
        elif type=='weibo':
            pass
        elif type=='163':
            pass
        else:
            print('暂无任务要操作')
if __name__ == '__main__':
    thread = MyHotThread('juejin')
    thread.start()