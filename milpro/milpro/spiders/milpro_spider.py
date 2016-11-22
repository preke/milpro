# coding: utf8
import scrapy
from scrapy.http import FormRequest
from scrapy.http import Request
import requests


class MilproSpider(scrapy.spiders.Spider):
    name = "mil"
    start_urls = [
        'http://search.mod.gov.cn/search/action/searchht.jsp'
    ]

    def start_requests(self):

            response = requests.post(
                'http://search.mod.gov.cn/search/action/searchht.jsp',
                data={
                    'basenames': 'gfb_sck_gdk_view',
                    'where':'TITLE=(国防部) and LANGUAGES=1 and publishstate=2',
                    'curpage':'1',
                    'pagecount':'20',
                    'classvalue1':'ALL',
                    'classfield1':'NODESEARCHNAME',
                    'classvalue2':'ALL',
                    'classfield2':'CLASS2',
                    'classvalue3':'ALL',
                    'classfield3':'CLASS',
                    'isclass':'1',
                    'istong':'0',
                    'searchList':'TITLE,CONTENT,AUTHOR,DOCURL,SOURCE,CLASS1,CLASS2,KEYWORD,IMAGE,DOCTYPE,LANGUAGES,SITENAME,INPUTTIME,PUBLISH',
                    'keyword':'国防部',
                    'znkz':'0',
                    'sortfield':'-INPUTTIME',
                    'searchtype':'normal',
                    'fantiorjianti':'0',
                    'id':'0.6963894961398835',
                    '_':''

                }
            )
            return [self.parse(response)]

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.text.encode('utf-8'))