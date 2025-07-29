import sys,os,re,json
from .AIQA import AIQA
from .AIQAResponse import AIQAResponse
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from model.models.DouBaoModelFactory import DouBaoModelFactory
from loginer.factory.DouBaoLoginerFactory import DouBaoLoginerFactory   

class DouBaoQA(AIQA):
  
  def __init__(self,question):
    # { AIQASchema }
    material = {'question':question}
    model = DouBaoModelFactory().create_qa(material)
    # { Loginer } set loginer for relogin
    loginer = DouBaoLoginerFactory().create_persistent_mac()

    super().__init__(model,loginer)
