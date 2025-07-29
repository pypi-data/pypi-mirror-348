from .ReaderSchemaCreator import ReaderSchemaCreator

class SchemaCreatorChain():

  def handle(self,schema_dict):
    handler = self.__get_chain()
    return handler.handle(schema_dict)

  def __get_chain(self):
    '''
    Converters must be executed sequentially
    '''
    # writer
    reader_creator = ReaderSchemaCreator()

    return reader_creator
