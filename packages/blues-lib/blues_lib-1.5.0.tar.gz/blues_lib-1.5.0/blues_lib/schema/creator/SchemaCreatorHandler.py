from abc import ABC,abstractmethod

class SchemaCreatorHandler(ABC):

  def __init__(self):
    '''
    The abstract class of handlers 
    '''
    self._next_handler = None
  
  def set_next(self,handler):
    '''
    Set the next handler
    '''
    self._next_handler = handler
    return handler

  def handle(self,schema_dict):
    '''
    @param {dict} schema_dict : the schema's schema_dict dict
    '''
    schema = self.resolve(schema_dict)
    if not schema and self._next_handler:
      return self._next_handler.handle(schema_dict)
    else:
      return schema

  @abstractmethod
  def resolve(self,schema_dict):
    pass
