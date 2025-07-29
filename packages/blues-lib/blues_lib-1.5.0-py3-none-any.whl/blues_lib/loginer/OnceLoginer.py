import sys,os,re
from abc import ABC,abstractmethod
from .Loginer import Loginer
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.browser.BrowserFactory import BrowserFactory     

class OnceLoginer(Loginer,ABC):
  '''
  @description: In a single login, the Browser instance is returned without saving the cookie
  '''

  def set_browser(self):
    executable_path = self.schema.browser.get('path')
    browser_mode = self.schema.browser.get('mode')
    self.browser = BrowserFactory(browser_mode).create(executable_path=executable_path)
    
  def success(self):
    self._logger.info('Login successfully')
    return self.browser
