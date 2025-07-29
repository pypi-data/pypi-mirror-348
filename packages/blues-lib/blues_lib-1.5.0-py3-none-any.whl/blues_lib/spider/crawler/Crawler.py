import sys,re,os,json
from abc import ABC,abstractmethod
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.browser.BrowserFactory import BrowserFactory     
from spider.deco.LogDeco import LogDeco

class Crawler(ABC):
  
  def __init__(self,request):
    self.request = {
      **self.get_request(request),
      "browser":self._get_browser(request['schema'])
    }
    self.message = ''

  def _get_browser(self,schema):
    executable_path = schema.browser.get('path')
    browser_mode = schema.browser.get('mode')
    return BrowserFactory(browser_mode).create(executable_path=executable_path)
    
  @LogDeco()
  def crawl(self):
    crawl_chain = self.get_chain()
    crawl_chain.handle(self.request)
    self.request['browser'].quit()
    self.message = self.get_message()
    return self.get_items()
    
  @abstractmethod
  def get_request(self):
    '''
    Template method: get the mixed request
    '''
    pass

  @abstractmethod
  def get_chain(self):
    '''
    Template method: get the crawl chain
    '''
    pass

  @abstractmethod
  def get_items(self):
    '''
    Template method: get the return value from the request
    '''
    pass
  
  @abstractmethod
  def get_message(self):
    '''
    Template method: get the log message
    '''
    pass
  