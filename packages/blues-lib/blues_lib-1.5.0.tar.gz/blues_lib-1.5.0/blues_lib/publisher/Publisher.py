import sys,os,re,time
from abc import ABC,abstractmethod
from .releaser.ReleaserFactory import ReleaserFactory
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.browser.BluesLoginChrome import BluesLoginChrome    
from sele.cleanup.CleanupChain import CleanupChain     
from util.BluesConsole import BluesConsole
from util.BluesDateTime import BluesDateTime

class Publisher(ABC):

  def __init__(self,models,loginer=None):
    # {list<dict>} : {'schema':xxx,'material':xx}
    self.models = models
    # { Loginer } the site's loginer
    self.loginer = loginer
    # { BluesLoginChrome } login auto
    self.browser = None
  
  def publish(self):
    '''
    @description : the final method
    '''
    self.ready()
    self.execute(False)
    self.quit()

  def preview(self):
    '''
    @description : the final method
    '''
    self.ready()
    self.execute()
    time.sleep(10)
    self.quit()
    
  def ready(self):
    self.check()
    self.login()
  
  def execute(self,is_preview=True):
    models = self.__get_models()
    for model in models:
      self.execute_one(model,is_preview)
      
  def execute_one(self,model,is_preview):
    schema = model['schema']
    factory = ReleaserFactory()
    releaser = factory.create(self.browser,schema)
    if releaser:
      if is_preview:
        releaser.preview()
      else:
        releaser.release()
        self.verify(model)
        BluesDateTime.count_down({'duration':5,'title':'Cleanup after 5 seconds'})
        self.cleanup(model)
    else:
      BluesConsole.info('No available releaser for channel: %s' % schema.CHANNEL)

  def __get_models(self):
    return self.models if type(self.models)==list else [self.models]

  def check(self):
    if not self.models:
      raise Exception('No available models')

  def login(self):
    self.browser = BluesLoginChrome(self.loginer)

  def quit(self):
    if self.browser:
      self.browser.quit()

  def verify(self,model):
    '''
    Verify whether the publication is successful.
    If the publication is successful and the page jumps, then the publishing button element will not exist.
    '''
    # Use the form page's submit element to make sure weather published succesfully
    schema = model['schema'] 
    material = model['material'] 
    url = schema.url_atom.get_value()
    if self.browser.waiter.ec.url_changes(url,10):
      material['material_status'] = 'pubsuccess'
    else:
      material['material_status'] = 'pubfailure'
    
  def cleanup(self,model):
    schema = model['schema']
    material = model['material']
    request = {
      'browser':self.browser,
      'material':material,
      'log':{
        'pub_platform':schema.PLATFORM,
        'pub_channel':schema.CHANNEL,
      },
      'validity_days':30,
    }
    chain = CleanupChain()
    chain.handle(request)
    



  
