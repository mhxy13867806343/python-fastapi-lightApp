from sqlalchemy.orm import Session,sessionmaker
from fastapi import APIRouter, FastAPI, Depends, File, UploadFile, Form
import requests
import time
import json
import schedule
from pyquery import PyQuery as pq
import threading
from extend.db import ENGIN
from models.dicts.dicts_model import CrawlerHot,DictsDict
LOCSESSION=sessionmaker(bind=ENGIN)
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
            downZhihu(_db,type)
        elif type=='baidu':
            downBaidu(_db,type)
        elif type=='weixin':
            pass
        elif type=='weibo':
            pass
        elif type=='163':
            pass
        else:
            print('暂无任务要操作')
def downZhihu(db:Session,type='zhihu'):
    url = "https://www.zhihu.com/billboard?utm_id=0"
    res = requests.get(url)
    t = pq(res.text).find('#js-initialData').text()
    hotList = json.loads(t)['initialState']['topstory']['hotList']
    for item in hotList:
        Qsplt=item['cardId'].split('Q_')[-1]
        cardIdUrl = f"https://www.zhihu.com/question/{Qsplt}?utm_division=hot_list_page&utm_id=0"

        cardId = item['cardId']

        answerCount = item['feedSpecific']['answerCount']
        text = item['target']['titleArea']['text']
        print(cardIdUrl, cardId, answerCount, text)
        kw = {
            'hot_count': answerCount, 'hot_cid':cardId, 'hot_url': cardIdUrl, 'hot_time':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            'hot_name': text
        }
        saveKwargsDb(db, type, **kw)
def saveKwargsDb(db,type,**kwargs):
    hot_count=kwargs['hot_count']
    hot_cid=kwargs['hot_cid']
    hot_url=kwargs['hot_url']
    hot_time=kwargs['hot_time']
    hot_name=kwargs['hot_name']
    cursor = db.query(
        CrawlerHot
    ).filter(CrawlerHot.hot_cid ==hot_cid).first()
    dictsId = db.query(DictsDict).filter(DictsDict.key_value == type).first()
    if cursor is None:
        db.add(CrawlerHot(hot_cid=hot_cid,
                          hot_type=type,
                          hot_name=hot_name, hot_count=hot_count, hot_url=hot_url, hot_time=hot_time,
                          dict_id=(dictsId and dictsId.id) or (0)
                          ))
        db.commit()
        db.flush()
    else:
        cursor.hot_count = hot_count
        cursor.hot_type = type or 'juejin'
        cursor.hot_url = hot_url
        cursor.hot_name =hot_name
        cursor.hot_cid =hot_cid
        cursor.dict_id = (dictsId and dictsId.id) or (0)
        db.commit()
        db.flush()
def downBaidu(db:Session,type='baidu'):
    url = "https://top.baidu.com/board?tab=realtime"
    headers = {
        "cookie": 'BAIDUID=34CE5BEF628A5A357AB5A842D218D6DE:FG=1; BIDUPSID=34CE5BEF628A5A357AB5A842D218D6DE; PSTM=1665212150; newlogin=1; BDUSS=V1Uk1pWmdEbVdufnFmeGhBVmFOdHVabDNncFhQV0s5ZEhYMXprYmVRR2FDYWxqSVFBQUFBJCQAAAAAAQAAAAEAAABzz6wEwfW0usvJMTk5MDEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJp8gWOafIFjeD; BDUSS_BFESS=V1Uk1pWmdEbVdufnFmeGhBVmFOdHVabDNncFhQV0s5ZEhYMXprYmVRR2FDYWxqSVFBQUFBJCQAAAAAAQAAAAEAAABzz6wEwfW0usvJMTk5MDEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJp8gWOafIFjeD; BAIDUID_BFESS=34CE5BEF628A5A357AB5A842D218D6DE:FG=1; delPer=0; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; BDORZ=FAE1F8CFA4E8841CC28A015FEAEE495D; BDPASSGATE=IlPT2AEptyoA_yiU4VKG3kIN8ejzTv_4D3OGSFppQ6W4fCaWmhH3U0VlMjPHTnOZHpD6xpWroBpcaV7eLz6q82J2xh1EeG-Sb5iM9s7KuLvmSaNg8bIZCb4jKUE2sBXKkRFaxgoT_fxGU79DyObcjvEHivKl73JQb4r55EDCkMe0_kGoDH8PxGyY28YJC7XfYcyO94rXnEpKKSmBUuL2KzS2gS1hOyAr8am8js221fjd6EoXGurSRvAa1G85I9pfG3bfGtuAzMS8ByUvrpsmVjwdokSI9uDvQk-Z; H_WISE_SIDS=110085_114550_132547_188747_204918_211986_213043_213357_214806_215727_216844_216941_219623_219943_219946_222624_223064_224045_224047_224436_226628_227932_228650_228866_229154_229905_229913_229967_230241_230930_231482_231496_231761_231904_231979_232551_232909_232959_233074_233466_233518_233598_233720_233837_234020_234044_234315_234350_234425_234514_234520_234560_234690_234721_234801_234925_234954_235160_235180_235415_235484_235534_235545_235587_235633_235897_235979_236021_236053_236084_236102_236237_236269_236296_236396_236408_236511_236516_236524_236527_236653_236788_236941_236998_237241_237254_237255_237448_237451_237459_237470_237527_237701_237777_237806; SE_LAUNCH=5%3A1669790219; BA_HECTOR=84a0842g8180000l8h048ivj1hodugb1h; PSINO=5',
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/106.0.0.0",
    }
    res = requests.get(url, headers=headers)
    pq_content = pq(res.content.decode('utf-8'))
    cc = pq_content.find('.SN-WEB-waterfall-item ._1HDqy7CiCHyZp5GKaGf2qa .row-start-center').items()
    for index,item in enumerate(cc):
        hot_name=item.find('._38vEKmzrdqNxu0Z5xPExcg').text()
        hot_url = f"https://m.baidu.com/s?word={hot_name}&sa=fyb_news"
        kw = {
            'hot_count': 0, 'hot_cid':f"{type}-{index+1}", 'hot_url': hot_url,
            'hot_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            'hot_name': hot_name
        }
        saveKwargsDb(db, type, **kw)
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
        kw={
            'hot_count':item['count'],  'hot_cid':item['id'], 'hot_url':item['url'], 'hot_time': item['time'], 'hot_name': item['name']
        }
        saveKwargsDb(db,type,**kw)


def main(type:str='juejin'):
    print('开始获取时间为:',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    thread = MyHotThread(type)
    thread.start()
    print('结束获取时间为:', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
def crawlerJob(type:str='juejin',num=24,sl=1):
    print('定时获取')
    print('获取数据类型',type)
    print('开始获取时间为:',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print(f'每次获取{num}时间的数据')
    print(f'每次获取间隔{sl}秒')
    schedule.every(num).hours.do(main, type=type)
    n=0
    while True:
        n += 1
        print(f'正在从{type}中获取数据...')
        time.sleep(1)
        print(f'第{n}次获取')
        schedule.run_pending()
        time.sleep(sl)


if __name__ == '__main__':
    crawlerJob('juejin')
    crawlerJob('zhihu')
    crawlerJob('baidu')