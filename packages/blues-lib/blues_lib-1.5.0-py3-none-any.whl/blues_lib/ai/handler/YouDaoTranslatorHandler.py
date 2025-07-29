import sys,os,re,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from ai.YouDaoQA import YouDaoQA
from ai.handler.AIHandleQuestion import AIHandleQuestion
from ai.handler.rule.AIHandleRuleFactory import AIHandleRuleFactory
from util.BluesConsole import BluesConsole

class YouDaoTranslatorHandler():
  '''
  This class writer the input news
  '''
  
  def __init__(self,material):
    '''
    Translate all of the material's fields
    param {dict} material
    '''
    # {str}
    self.material = material
    # {int}
    self.retry_count = 0
    self.max_retry_count = 3

  def translate(self):
    if not self.material:
      return None

    item = {} 
    for key, value in self.material.items():
      item[key] = self.translate_one(value)
    return item

  def translate_one(self,text):
    '''
    Translate and output
    Return {str} 
    '''
    self.retry_count = 0
    # {AIHandleRule}
    rule = AIHandleRuleFactory.create('translate')
    # {AIQA}
    ai = YouDaoQA(text)
    return self.__retry(ai,rule)

  def __console(self,response):
    stat = 'successful' if response else 'failure'
    BluesConsole.info('The qa was %s' % stat)

  def __retry(self,ai,rule,response=None):
    if rule.is_response_valid(response):
      self.__console(response)
      return response 

    if self.retry_count > rule.max_retry_count:
      self.__console(None)
      return None

    if self.retry_count>1:
      BluesConsole.info('The response is invalid, retry: %s' % self.retry_count)
    response = ai.execute()
    self.retry_count+=1
    return self.__retry(ai,rule,response)
