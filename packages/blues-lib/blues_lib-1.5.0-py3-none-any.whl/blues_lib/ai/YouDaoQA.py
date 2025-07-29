import sys,os,re,json
from .AIQA import AIQA
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from model.models.YouDaoModelFactory import YouDaoModelFactory
from sele.browser.BluesStandardChrome import BluesStandardChrome

class YouDaoQA(AIQA):
  
  def __init__(self,question):
    # { AIQASchema }
    material = {'question':question}
    model = YouDaoModelFactory().create_translator(material)
    # Don't need to login
    loginer = None
    # must use headable driver, or copy failure
    browser = BluesStandardChrome()

    super().__init__(model,loginer,browser)
