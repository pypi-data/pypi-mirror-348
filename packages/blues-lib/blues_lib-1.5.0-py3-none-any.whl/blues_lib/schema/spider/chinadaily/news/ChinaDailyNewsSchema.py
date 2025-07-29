import sys,re,os
from abc import ABC,abstractmethod
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.reader.NewsReaderSchema import NewsReaderSchema

class ChinaDailyNewsSchema(NewsReaderSchema,ABC):

  def __init__(self):
    super().__init__()

    # the source site
    self.site = 'chinadaily'

    # the source lang
    self.lang = 'en'
    
    self.material_atom = self.__get_material_atom()

  def __get_material_atom(self):
    '''
    All news material has the same atom strcture
    '''
    # para atom
    para_unit_selector = '#Content>p,#Content>figure'
    para_field_atoms = [
      # use the para selector
      self._atom_factory.createText('text',''),
      self._atom_factory.createAttr('image','img','data-lazyload'),
    ]
    para_array_atom = self._atom_factory.createArray('para fields',para_field_atoms,pause=0) 
    para_atom = self._atom_factory.createPara('material_body',para_unit_selector,para_array_atom) 
    
    # outer atom
    container_selector = '#lft-art'
    field_atoms = [
      self._atom_factory.createText('material_title','h1'),
      self._atom_factory.createText('material_post_date','.info_l'),
      para_atom,
    ]
    array_atom = self._atom_factory.createArray('fields',field_atoms,pause=0) 
    return self._atom_factory.createNews('news',container_selector,array_atom) 
