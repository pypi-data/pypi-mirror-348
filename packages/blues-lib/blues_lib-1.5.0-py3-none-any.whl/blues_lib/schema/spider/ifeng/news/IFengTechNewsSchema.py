from .IFengNewsSchema import IFengNewsSchema

class IFengTechNewsSchema(IFengNewsSchema):
  
  def __init__(self):
    super().__init__()

    self.brief_url_atom = self._atom_factory.createURL('brief url','https://tech.ifeng.com/')
    
    self.brief_atom = self.__get_brief_atom()

  def __get_brief_atom(self):
    unit_selector = 'div[class^=index_hotEvent] a[class^=index_content]'
    field_atoms = [
      self._atom_factory.createAttr('material_title','.index_text_content_cdolu','title'),
      self._atom_factory.createAttr('material_url','','href'), # get from the unit element
      self._atom_factory.createAttr('material_thumbnail','img','src')
    ]
    array_atom = self._atom_factory.createArray('fields',field_atoms,pause=0) 
    return self._atom_factory.createBrief('briefs',unit_selector,array_atom) 

