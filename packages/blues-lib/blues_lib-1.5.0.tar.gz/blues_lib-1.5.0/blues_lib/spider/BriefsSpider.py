import sys,re,os,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from spider.Spider  import Spider  
from spider.crawler.CrawlerFactory import CrawlerFactory

class BriefsSpider(Spider):
  '''
  Just get the brief list, but the item is not a valid material, won't save to the DB
  '''

  def get_crawler(self,request):
    return CrawlerFactory(request).create_briefs()
