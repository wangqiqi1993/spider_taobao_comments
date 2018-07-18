'''spider taobao store comment
store url:https://detail.tmall.com/item.htm?id=18932210296,the import argument is id.
'''
import json
import requests
import time
import os
import uuid
import redis
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from config import *
img_path='/root/wcl2/taobao_comment/comment_imgs'
if not os.path.exists(img_path):
    os.makedirs(img_path)
def getComments(url):
    commentlist=[]
    response = '{' + requests.get(url).text.strip() + '}'
    jd=json.loads(response)
    comment_list=jd['rateDetail']['rateList']
    for comment in comment_list:
        dict = {}
        try:
            dict['description_goods']=comment['auctionSku']#description goods,such as the color,the style
            dict['rateContent']=comment['rateContent']
            try:
                dict['imgs']=comment['pics']
            except:
                print('without comment imgs')
        except:
            print('no comment')
        commentlist.append(dict)
    return commentlist
def save_info(info):
    for ele in info:
        #ele:dict
        with open('/root/wcl2/taobao_comment/comment.csv','a')as fp:
            fp.write(ele['description_goods']+'\t')
            fp.write(ele['rateContent'].replace('\ufffd','')+'\n')
        for img in ele['imgs']:
            if not img.startswith('http:'):
                img='http:'+img
            # img_name=str(uuid.uuid1()).replace('-','_')+'.jpg'
            # with open(os.path.join(img_path,img_name),'wb+')as f:
            #     f.write(requests.get(img).content)
                r.sadd(img_url,img)
if __name__=='__main__':
    '''the important parameters:itemID,spuId'''
    r=redis.Redis(host=redis_host,port=redis_port,db=redis_db,password=password)
    start_url='https://rate.tmall.com/list_detail_rate.htm?itemId=18932210296&spuId=0&sellerId=1669252141&order=3&currentPage={0}&_ksTS={1}'
    ksTS=str(time.time()*1000).replace('.','_')
    for page in range(1,2):
        url=start_url.format(page,ksTS)
        info=getComments(url)#return list
        save_info(info)

