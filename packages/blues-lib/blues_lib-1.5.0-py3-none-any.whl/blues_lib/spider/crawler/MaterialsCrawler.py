import sys,re,os,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from spider.crawler.Crawler import Crawler 
from spider.chain.CrawlerChain  import CrawlerChain  

class MaterialsCrawler(Crawler):
  '''
  Get multi materials, get brief first then get article automatically
  '''
  
  def get_request(self,request):
    return {
      'briefs':None, # as the output
      'materials':None, # as the output
      'schema':None, # required
      'max_material_count':1,
      'max_material_image_count':9,
      'min_content_length':150,
      'max_content_length':10000,
      **request,
    }

  def get_chain(self):
    return CrawlerChain()

  def get_items(self):
    return self.request.get('materials')

  def get_message(self):
    items = self.get_items()
    count = len(items) if items else 0
    message = 'Crawled [%s] materials totally' % count
    if count>0:
      message+=self.__get_titles(items)
    return message

  def __get_titles(self,items):
    titles = ''
    i = 1
    for item in items:
      titles+='\n %s. %s' % (i,item.get('material_title'))
      i+=1
    return titles