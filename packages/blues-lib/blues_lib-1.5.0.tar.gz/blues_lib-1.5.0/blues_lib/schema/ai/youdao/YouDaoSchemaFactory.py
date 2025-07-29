import sys,os,re,json
from .YouDaoTranslatorSchema import YouDaoTranslatorSchema

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.ai.AISchemaFactory import AISchemaFactory

class YouDaoSchemaFactory(AISchemaFactory):

  def create_translator(self):
    return YouDaoTranslatorSchema()
