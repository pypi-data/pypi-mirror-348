import sys,re,os,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from spider.crawler.Crawler import Crawler 
from spider.chain.brief.BriefCrawlerChain  import BriefCrawlerChain  

class BriefsCrawler(Crawler):
  '''
  Get a breif list
  '''
  
  def get_request(self,request):
    return {
      'briefs':None, # as the result
      'schema':None, # required
      **request,
    }

  def get_chain(self):
    return BriefCrawlerChain()

  def get_items(self):
    return self.request.get('briefs')

  def get_message(self):
    site = self.request['schema'].basic.get('site')
    items = self.get_items()
    count = len(items) if items else 0
    message = 'Crawled [%s] available items from %s' % (count,site)
    if count>0:
      message+=self.__get_titles(items)
      message+=self.__get_item(items[0])
    return message

  def __get_titles(self,items):
    titles = ''
    i = 1
    for item in items:
      titles+='\n %s. %s' % (i,item.get('material_title'))
      i+=1
    return titles
  
  def __get_item(self,item):
    return "\n\nExample:\n%s" % json.dumps(item, indent=2, ensure_ascii=False)