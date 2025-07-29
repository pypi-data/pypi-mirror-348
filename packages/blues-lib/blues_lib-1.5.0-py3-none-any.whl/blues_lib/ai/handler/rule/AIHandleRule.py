import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from ai.AIQAResponse import AIQAResponse
from util.BluesConsole import BluesConsole

class AIHandleRule():

  def __init__(self,min_text_len=1,max_retry_count=3):
    self.min_text_len = min_text_len
    self.max_retry_count = max_retry_count

  def is_response_valid(self,text) :
    text_error = self.__get_len_error(text,self.min_text_len)
    if text_error:
      BluesConsole.error(text_error)
      return False
    return True
    
  def __get_len_error(self,text,min_len):
    error = ''
    text_len = self.__get_length(text)
    if text_len < min_len:
      error = 'The text does not reach the minimum length (%s/%s)' % (text_len,min_len)
    return error
  
  def __get_length(self,text):
    length = 0
    if not text:
      return length

    for char in text:
      # 判断是否为中文字符（Unicode范围）
      if '\u4e00' <= char <= '\u9fff':
        length += 1
      # 非中文字符（包括英文、数字、标点符号等）
      else:
        length += 0.5
    return length