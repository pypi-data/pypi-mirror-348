import sys,re,os
from .news.ChinaDailyAmericaSchema import ChinaDailyAmericaSchema

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.reader.ReaderSchemaFactory import ReaderSchemaFactory

class ChinaDailySchemaFactory(ReaderSchemaFactory):

  def create_news_schemas(self):
    return [
      self.create_america(),
    ]

  def create_america(self):
    return ChinaDailyAmericaSchema()