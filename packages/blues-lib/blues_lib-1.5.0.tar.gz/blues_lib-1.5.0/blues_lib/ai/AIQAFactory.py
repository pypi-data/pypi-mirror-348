from .DouBaoQA import DouBaoQA
from .DouBaoArticleQA import DouBaoArticleQA
from .DouBaoImgGen import DouBaoImgGen
from .DeepSeekArticleQA import DeepSeekArticleQA

class AIQAFactory():

  @classmethod
  def create(self,name,question):
    '''
    Get a AIQA instance
    param {str} name : the ai name
    param {str} question : the ai's input str
    '''
    if name == 'doubao':
      return DouBaoQA(question)
    elif name == 'doubao_article':
      return DouBaoArticleQA(question)
    elif name == 'doubao_img_gen':
      return DouBaoImgGen(question)
    elif name == 'deepseek_article':
      return DeepSeekArticleQA(question)
    else:
      return DouBaoQA(question)