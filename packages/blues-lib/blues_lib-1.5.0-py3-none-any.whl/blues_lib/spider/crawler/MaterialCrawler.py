import sys,re,os,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from spider.crawler.Crawler import Crawler 
from spider.chain.material.MaterialCrawlerChain  import MaterialCrawlerChain  

class MaterialCrawler(Crawler):
  '''
  Get a specify article
  @param {dict} request.brief : a standard brief object, such as:
    {'material_title': '特朗普：征收100%关税，立即启动', 'material_url': 'https://news.ifeng.com/c/8j6HpVVa5Yu', 'material_thumbnail': None, 'material_type': 'news', 'material_site': 'ifeng', 'material_lang': 'cn', 'material_id': 'ifeng_5ca249f73162b2c77103b4bef9c3b946'}
  @returns {list|None} : return a material object list or None
  '''

  def get_request(self,request):
    return {
      'brief':None, # required, as the input
      'material':None, # as the output
      'schema':None, # required
      'max_material_image_count':9,
      'min_content_length':150,
      'max_content_length':10000,
      **request,
    }
  
  def get_chain(self):
    return MaterialCrawlerChain()

  def get_items(self):
    material = self.request.get('material')
    return [material] if material else None
  
  def get_message(self):
    items = self.get_items()
    if not items:
      message = 'Crawled material failure'
    else:
      message = 'Crawled material successfully' 
      message+=self.__get_item(items[0])
    return message
  
  def __get_item(self,item):
    article = '\n\nArticle :'
    article += "\n\n%s" % item['material_title']
    
    body = json.loads(item['material_body'])
    body = json.dumps(body, indent=2, ensure_ascii=False)
    article += "\n%s" % body
    return article