# coding: utf8
import scrapy
from scrapy.http import FormRequest
from scrapy.http import Request
import requests
from lxml import etree
from milpro.items import MilproItem
import hashlib
from scrapy.selector import Selector
from scrapy.http import XmlResponse
import urllib2
import urlparse
from bs4 import BeautifulSoup
import codecs
import re
import pymongo



class MilproSpider(scrapy.spiders.Spider):
    name = "mil"
    # start_urls = [
    #     'http://search.mod.gov.cn/search/action/searchht.jsp'
    # ]
    strs = ['军民融合',
            # '军民结合',
            # '寓军于民',
            # '军转民',
            # '民参军',
            # '两用技术',
            # '两用产业',
            # '国防科技工业',
            # '武器装备',
            # '军事装备',
            # '后勤装备',
            # '国防科技',
            # '国防工业',
            # '军事工业',
            # '国防经济',
            # '军事经济',
            # '国防建设与经济建设',
            # '装备采办',
            # '军品市场',
            # '装备市场',
            # '保障社会化',
            # '社会化保障',
            # '国防科研',
            # '军事科研',
            # '装备科研',
            # '军品采购',
            # '装备预研',
            # '装备维修',
            # '装备建设',
            # '装备发展',
            # '装备保障',
            # '空域管制',
            # '空域管理',
            # '电磁频谱管理',
            # '无线电管理',
            # '军事人才培训',
            # '国防生',
            # '基础设施建设',
            # '国防知识产权',
            '军民一体化'
            ]
    count = -1
    client = pymongo.MongoClient('0.0.0.0',27017)
    db = client.milpro
    collection = db.collection

    def start_requests(self):
        ans = []
        for s in self.strs:
            request = requests.post(
                'http://search.mod.gov.cn/search/action/searchht.jsp',
                data={
                    'basenames': 'gfb_sck_gdk_view',
                    'where':'TITLE=('+ s +') and LANGUAGES=1 and publishstate=2',
                    'curpage':'1',
                    'pagecount':'9999',
                    'classvalue1':'ALL',
                    'classfield1':'NODESEARCHNAME',
                    'classvalue2':'ALL',
                    'classfield2':'CLASS2',
                    'classvalue3':'ALL',
                    'classfield3':'CLASS',
                    'isclass':'1',
                    'istong':'0',
                    'searchList':'TITLE,CONTENT,AUTHOR,DOCURL,SOURCE,CLASS1,CLASS2,KEYWORD,IMAGE,DOCTYPE,LANGUAGES,SITENAME,INPUTTIME,PUBLISH',
                    'keyword':s,
                    'znkz':'0',
                    'sortfield':'-INPUTTIME',
                    'searchtype':'normal',
                    'fantiorjianti':'0',
                    'id':'0.6963894961398835',
                    '_':''
                }
            )
            ans.append(request)


        ans_total = []

        for a in ans:
            self.parse(a)

        return tuple(ans)


    # _id = scrapy.Field()
    # title = scrapy.Field()
    # source = scrapy.Field()
    # date = scrapy.Field()
    # author = scrapy.Field()
    # url = scrapy.Field()
    # content = scrapy.Field()
    # readnum = scrapy.Field()
    # commentNum = scrapy.Field()
    # isHandled = scrapy.Field()
    # keywords = scrapy.Field()
    # abstract = scrapy.Field()
    # event = scrapy.Field()


    def get_content(self, url):
        response = urllib2.urlopen(url)

        text = response.read()
        soup = BeautifulSoup(text, 'html.parser', from_encoding='utf-8')
        ans = ''
        zi = soup.find('div', class_='zi')
        ps = zi.find_all('p')
        for p in ps:
             ans = ans + p.get_text()

        return ans

    def parse(self, response):
        # print 'iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiitem'
        self.count += 1
        filename = str(self.count) + '.xml'
        with open(filename, 'wb') as f:
            f.write(response.text.encode('utf-8'))


        xml_file = etree.parse(filename)
        root_node = xml_file.getroot()
        results = root_node.xpath('//RESULT')
        for sub_root in results:
            item = MilproItem()
            item['title'] = sub_root.find('TITLE').text
            item['source'] = sub_root.find('SOURCE').text
            item['date'] = sub_root.find('PUBLISHTIME').text
            item['author'] = sub_root.find('AUTHOR').text
            item['url'] = sub_root.find('URL').text
            try:
                item['content'] = self.get_content( sub_root.find('URL').text )
            except:
                item['content'] = sub_root.find('CONTENT').text

            item['readNum'] = ''
            item['commentNum'] = ''
            item['isHandled'] = ''
            item['keywords'] = sub_root.find('KEYWORD').text
            item['abstract'] = sub_root.find('CONTENT').text
            item['event'] =''
            item['_id'] = hashlib.sha1(str(sub_root.find('TRSID').text)).hexdigest()
            self.collection.insert(item)
            #yield item






