# coding:utf-8
from lxml import etree
import codecs
import re  

  

if __name__ == '__main__':
	#f = open('1.xml', 'r')
	xml_file = etree.parse(r'1.xml')
	root_node = xml_file.getroot()
	results = root_node.xpath('//RESULT')
	for sub_root in results:
		print sub_root.find('TITLE').text

