import sys,re,os
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from spider.Spider import Spider  
from spider.crawler.CrawlerFactory import CrawlerFactory

class MaterialsSpider(Spider):
  '''
  Get the valid material list, use to crawl the info that don't need to go to the detail page
  Such as gallery list.
  '''
  def get_crawler(self,request):
    return CrawlerFactory(request).create_materials()