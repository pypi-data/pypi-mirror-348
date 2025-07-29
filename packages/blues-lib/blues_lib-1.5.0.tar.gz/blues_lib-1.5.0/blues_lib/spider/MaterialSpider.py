import sys,re,os,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from spider.Spider import Spider  
from spider.crawler.CrawlerFactory import CrawlerFactory

class MaterialSpider(Spider):
  '''
  Get the full material, go list page and go the detail page
  '''
  def get_crawler(self,request):
    return CrawlerFactory(request).create_material()
