import sys,re,os,json
from abc import ABC,abstractmethod
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from config.ConfigManager import config
from sele.browser.BluesStandardChrome import BluesStandardChrome
from sele.browser.BluesHeadlessChrome import BluesHeadlessChrome
from pool.BluesMaterialIO import BluesMaterialIO
from util.BluesLogger import BluesLogger 

class Spider(ABC):

  def __init__(self,request:dict):
    '''
    @param {dict} request
      - {ReaderSchema} schema [required]
      - {Browser} ChromeBrowser [required]
    '''
    self.request = request
    self._logger = BluesLogger.get_logger(__name__)

  def spide(self):
    '''
    Crawl and Quit and Save
    '''
    self.__set_browser()
    items = self.__crawl()
    return self.__save(items)
    
  def __crawl(self):
    '''
    Crawl and Quit
    '''
    crawler = self.get_crawler(self.request)
    return crawler.crawl()
    
  @abstractmethod
  def get_crawler(self,request):
    pass

  def __save(self,items):
    if not items:
      return 0

    result = BluesMaterialIO.insert(items)
    message = ''
    code = result.get('code')
    count = result.get('count',0)
    msg = result.get('message')
    if code == 200:
      message = 'Insert [%s] materials' % count
    else:
      message = 'Insert 0 materials, error: %s' % msg

    self._logger.info(message)
    return count

  def __set_browser(self):
    if self.request.get('browser'):
      return 

    browser = None
    headless = self.request.get('headless',True)
    webdriver_path = config.get("webdriver.path")
    if headless:
      browser = BluesHeadlessChrome(executable_path=webdriver_path)
    else:
      browser = BluesStandardChrome(executable_path=webdriver_path)
    self.request['browser'] = browser