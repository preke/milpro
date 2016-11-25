# coding: utf-8
import requests

import hashlib
import urllib2
import urlparse
from bs4 import BeautifulSoup
import codecs
import re
import pymongo
import json





if __name__ == '__main__':
    client = pymongo.MongoClient('127.0.0.1',27017)
    db = client.milpro
    collection = db.collection
    strs = [
        '军民融合',
        '军民结合',
        '寓军于民',
        '军转民',
        '民参军',
        '两用技术',
        '两用产业',
        '国防科技工业',
        '武器装备',
        '军事装备',
        '后勤装备',
        '国防科技',
        '国防工业',
        '军事工业',
        '国防经济',
        '军事经济',
        '国防建设与经济建设',
        '装备采办',
        '军品市场',
        '装备市场',
        '保障社会化',
        '社会化保障',
        '国防科研',
        '军事科研',
        '装备科研',
        '军品采购',
        '装备预研',
        '装备维修',
        '装备建设',
        '装备发展',
        '装备保障',
        '空域管制',
        '空域管理',
        '电磁频谱管理',
        '无线电管理',
        '军事人才培训',
        '国防生',
        '基础设施建设',
        '国防知识产权',
        '军民一体化'
        ]
    for s in strs:
        print s
        cnt = 0
        while (True):
            request = requests.post(
                'http://searchweb.miit.gov.cn/search/search',
                data={
                    'urls'     : 'http://www.miit.gov.cn/',
                    'sortKey'  : 'showTime',
                    'sortFlag' : '-1',
                    'fullText' : s,
                    'sortType' : '1',
                    'indexDB'  : 'css',
                    'pageSize' : '10',
                    'pageNow'  : cnt
                }
            )
            
            Json = request.json()
            if len(Json[u'array']) == 0:
                print 'ohhhh'
                break
            else:
                cnt += 1
                for j in Json[u'array']:
                    j1 = dict()
                    j1['_id']        =  hashlib.sha1(str(j[u'id'])).hexdigest()
                    j1['title']      =  j[u'name'].encode('utf-8')
                    j1['source']     = ''
                    j1['date']       = j[u'showTime'].encode('utf-8')
                    j1['author']     = ''
                    j1['url']        = j[u'url']
                    j1['content']    = j[u'summaries'].encode('utf-8')
                    j1['readnum']    = ''
                    j1['commentNum'] = ''
                    j1['isHandled']  = ''
                    j1['keywords']   = s
                    j1['abstract']   = j[u'summaries'].encode('utf-8')
                    j1['event']      = ''
                       
                    try:
                        collection.insert(j1)
                    except:
                        pass


