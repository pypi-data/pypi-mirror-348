import sys,os,re
from abc import ABC,abstractmethod
from .Loginer import Loginer
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.browser.BrowserFactory import BrowserFactory     
from util.BluesDateTime import BluesDateTime      

class PersistentLoginer(Loginer,ABC):

  def set_browser(self):
    proxy_config = self.schema.proxy
    cookie_config = self.schema.cookie
    executable_path = self.schema.browser.get('path')
    browser_mode = 'proxy'
    self.browser = BrowserFactory(browser_mode).create(proxy_config=proxy_config,cookie_config=cookie_config,executable_path=executable_path)
    
  def success(self):
    login_max_time = self.schema.basic.get('login_max_time')
    BluesDateTime.count_down({
      'duration':login_max_time,
      'title':'Requesting...'
    })

    cookie_file = self.browser.save_cookies()
    self.browser.interactor.navi.quit()

    if cookie_file:
      self._logger.info('Saved cookies to the file: %s' % cookie_file)
      return True
    else:
      self._logger.error('Saved cookies failure')
      return False
      
  