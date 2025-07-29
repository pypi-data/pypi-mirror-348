import sys,os,re,json
from .DouBaoQA import DouBaoQA
from .AIQAResponse import AIQAResponse
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from model.models.DouBaoModelFactory import DouBaoModelFactory
from loginer.factory.DouBaoLoginerFactory import DouBaoLoginerFactory   
from util.BluesConsole import BluesConsole

class DouBaoArticleQA(DouBaoQA):
  
  def extract(self,text):
    '''
    Extract format fields from the copied text
    '''
    # {list<str>} content is text copy from the clip board
    paras = self.__get_para_list(text)
    
    # the first line is the title
    title_para = paras.pop(0)
    title = self.__get_title(title_para)

    return AIQAResponse(title,paras)

  def __get_para_list(self,text):
    body = text.replace('"',"'")
    paras = re.split(r'[\n\r]', body)
    para_list = []
    for para in paras:
      text = para.strip()
      if text:
        para_list.append(text)
    return para_list

  def __get_title(self,title):
    patterns = [
      r'标题\s*[:：]?\s*(.+)', # 标题: xxx
      r'《(.+)》', # 标题：《xxx》
      r'\*+(.+)\*+', # **xxx**
    ]

    text = title
    for pattern in patterns:
      matches = re.findall(pattern,text)
      if matches:
        text = matches[0]

    # patter : ** xxx ** ; # xxxx
    return re.sub(r'[#*]', '', text).strip()

