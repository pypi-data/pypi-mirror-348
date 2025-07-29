import sys,os,re,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from model.decoder.DecoderHandler import DecoderHandler
from ai.handler.YouDaoTranslatorHandler import YouDaoTranslatorHandler

class ArticleTranslator(DecoderHandler):
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
    item = {
      'title':material['material_title'],
      'content':article,
    }
    handler = YouDaoTranslatorHandler(item)
    # {AIQAResponse}
    response = handler.translate()

    # save the original value to the ori field
    material['material_ori_title'] = material['material_title']
    material['material_ori_body_text'] = material['material_body_text']
    # use ai firstly
    title = response.get('title','')
    content = response.get('content','')
    if not title or not content:
      raise Exception('translate fialure')

    material['material_title'] = title
    material['material_body_text'] = self.__get_paras(content)
    
  def __get_paras(self,content):
    '''
    Convert the translated text to para list
    '''
    paras = []
    lines = re.split(r'[。]', content)
    para = ''
    for line in lines:
      para+=line.strip()+'。'
      if len(para)>=150:
        paras.append(para)
        para = ''
    return paras