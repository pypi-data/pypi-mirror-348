import sys,os,re,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from model.decoder.DecoderHandler import DecoderHandler
from ai.handler.AITranslatorHandler import AITranslatorHandler

class AITranslator(DecoderHandler):
  '''
  Extend the required fields by existed fields
  '''
  kind = 'handler'

  def resolve(self,request):
    if not request:
      return request

    material = request.get('material') 
    if not material or material.get('material_lang')!='en':
      return request
    
    self.__translate(request)
    return request
    
  def __get_article(self,material):
    paras = material.get('material_body_text')
    if not paras:
      return None
    return ''.join(paras)

  def __translate(self,request):
    material = request.get('material')
    article = self.__get_article(material)
    if not article:
      return

    # 头条会识别豆包的内容
    handler = AITranslatorHandler(article,'doubao_article')
    # {AIQAResponse}
    response = handler.article_translate()

    if response:
      # save the original value to the ori field
      material['material_ori_title'] = material['material_title']
      material['material_ori_body_text'] = material['material_body_text']
      # use ai firstly
      material['material_title'] = response.title
      material['material_body_text'] = response.content