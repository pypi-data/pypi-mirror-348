from .ChinaDailyNewsSchema import ChinaDailyNewsSchema

class ChinaDailyAmericaSchema(ChinaDailyNewsSchema):
  
  def __init__(self):
    super().__init__()

    self.brief_url_atom = self._atom_factory.createURL('brief url','https://www.chinadaily.com.cn/world/america')
    
    self.brief_atom = self.__get_brief_atom()

  def __get_brief_atom(self):
    unit_selector = '#left>.mb10'
    field_atoms = [
      self._atom_factory.createText('material_title','h4 a'),
      self._atom_factory.createAttr('material_url','h4 a','href'), 
      self._atom_factory.createAttr('material_thumbnail','img','src')
    ]
    array_atom = self._atom_factory.createArray('fields',field_atoms,pause=0) 
    return self._atom_factory.createBrief('briefs',unit_selector,array_atom) 

