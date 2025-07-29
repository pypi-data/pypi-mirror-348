from abc import ABC,abstractmethod

class LoginerFactory(ABC):
  '''
  Abstract Factory Mode, use best practices:
  1. Each specific class is created using an independent method
  2. Use instance usage and parameters as class fields
  '''
  
  def __init__(self,schema):
    self._schema = schema

  @abstractmethod
  def create_account(self):
    pass
  
  @abstractmethod
  def create_mac(self):
    pass
