import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.creator.SchemaCreatorHandler import SchemaCreatorHandler
from schema.reader.ReaderSchema import ReaderSchema
from atom.AtomCreator import AtomCreator

class ReaderSchemaCreator(SchemaCreatorHandler):
  
  def resolve(self,schema_dict):
    if schema_dict.get('category')!='reader':
      return None
    else:
      return self.create(schema_dict)

  def create(self,schema_dict):
    '''
    Base on a general dict to create a standard reader schema
    @param {dict} schema_dict : the whole schema schema_dict
    '''
    schema = ReaderSchema() 
    self.__set_system_fields(schema,schema_dict)
    self.__set_atom_fields(schema,schema_dict)
    return schema

  def __set_system_fields(self,schema,schema_dict):
    # the name of the sub reader class
    schema.type = schema_dict.get('type')
    # the name of the dealing site
    schema.site = schema_dict.get('site')
    # the lang of the dealing site
    schema.lang = schema_dict.get('lang','cn')
    
  def __set_atom_fields(self,schema,schema_dict):
  
    # { URLAtom } the list page url [required]
    schema.brief_url_atom = self.__get_atom(schema_dict,'brief_url')

    # { ArrayAtom } The actions that need to be performed before crawling the brief
    schema.before_brief_atom = self.__get_atom(schema_dict,'before_brief')

    # { BriefAtom } the brief atom [required]
    schema.brief_atom = self.__get_atom(schema_dict,'brief')

    # { ArrayAtom } 
    schema.after_brief_atom = self.__get_atom(schema_dict,'after_brief')

    # { ArrayAtom } the events before fetch material
    schema.before_material_atom = self.__get_atom(schema_dict,'before_material')

    # { ArticleAtom } the article atom
    schema.material_atom = self.__get_atom(schema_dict,'material')
    
    # { ArrayAtom }
    schema.after_material_atom = self.__get_atom(schema_dict,'after_material')

  def __get_atom(self,schema_dict,key):
    kwargs = schema_dict.get(key) # {dict}
    if not kwargs:
      return None

    return AtomCreator.create(kwargs)
