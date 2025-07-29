import sys,os,re,time
from abc import ABC,abstractmethod
from .AIQAResponse import AIQAResponse
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from loginer.OnceLoginer import OnceLoginer   
from sele.browser.BluesLoginChrome import BluesLoginChrome    
from sele.behavior.FormBehavior import FormBehavior       
from sele.behavior.BehaviorChain import BehaviorChain       
from util.BluesOS import BluesOS
from util.BluesDateTime import BluesDateTime
from util.BluesConsole import BluesConsole

class AIQA(ABC):
  
  def __init__(self,model,loginer=None,browser=None):
    # { AIQASchema }
    self.schema = model['schema']
    # {Dict}
    self.material = model['material']
    # { Loginer } set loginer for relogin
    self.loginer = loginer
    # {BluesLoginChrome}
    self.browser = browser

  def execute(self):
    '''
    Fianl tempalte method
    Input question and return answer
    Returns {json} : json string
    '''
    try:
      self.open()
      self.question()
      self.submit()
      self.wait()
      return self.answer()
    except Exception as e:
      BluesConsole.error(e)
      return None
    finally:
      self.browser.quit()

  def open(self):
    # don't login agin when retry
    if not self.browser:
      if isinstance(self.loginer,OnceLoginer):
        BluesConsole.info('Using once loginer')
        self.browser = self.loginer.login()
      else:
        self.browser = BluesLoginChrome(self.loginer)

    url = self.schema.url_atom.get_value()
    self.browser.open(url)
  
  def question(self):
    BluesConsole.info(self.material['question'])
    # contains fill atom and send atom
    popup_atom = self.schema.popup_atom
    question_atom = self.schema.question_atom
    handler = FormBehavior(self.browser,question_atom,popup_atom)
    handler.handle()

  def submit(self):
    popup_atom = self.schema.popup_atom
    submit_atom = self.schema.submit_atom
    if submit_atom:
      handler = FormBehavior(self.browser,submit_atom,popup_atom)
      handler.handle()

  def wait(self):
    pass

  def answer(self): 
    BluesOS.clear()

    answer_atom = self.schema.answer_atom
    handler = BehaviorChain(self.browser,answer_atom)
    handler.handle()

    text = BluesOS.copy()

    BluesConsole.info('AI outcome:  %s' % text)
    if not text:
      return None

    # {AIQAResponse} 
    response = self.extract(text)
    log_text = 'None' 
    if response:
      if isinstance(response,AIQAResponse):
        log_text = response.to_string()
      else:
        log_text = response
    BluesConsole.info('AI response:  %s' % log_text)
    return response
    
  def extract(self,text):
    '''
    Template method: cover this method by different ai platform
    '''
    return text
