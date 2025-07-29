from .IFengNewsSchema import IFengNewsSchema

class IFengTechOutpostSchema(IFengNewsSchema):
  
  def __init__(self):
    super().__init__()

    self.brief_url_atom = self._atom_factory.createURL('brief url','https://www.ifeng.com/')
    
    self.brief_atom = self.__get_brief_atom()

  def __get_brief_atom(self):
    unit_selector = '.index_center_box_vOlLP div:not(.index_news_list_DXAWc) p[class^=index_news_list_p]'
    field_atoms = [
      self._atom_factory.createAttr('material_title','a','title'),
      self._atom_factory.createAttr('material_url','a','href'), # get from the unit element
      self._atom_factory.createAttr('material_thumbnail','img','src')
    ]
    array_atom = self._atom_factory.createArray('fields',field_atoms,pause=0) 
    return self._atom_factory.createBrief('briefs',unit_selector,array_atom) 

