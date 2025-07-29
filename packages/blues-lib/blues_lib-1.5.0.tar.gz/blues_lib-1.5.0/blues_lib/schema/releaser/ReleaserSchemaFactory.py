from .NewsReleaserSchema import NewsReleaserSchema
from .GalleryReleaserSchema import GalleryReleaserSchema
from .EventsReleaserSchema import EventsReleaserSchema

class ReleaserSchemaFactory():

  @classmethod
  def create(cls,meta:dict):
    
    schema_type = meta.get('type')

    if schema_type == 'news':
      return NewsReleaserSchema(meta)
    elif schema_type == 'gallery':
      return GalleryReleaserSchema(meta)
    elif schema_type == 'events':
      return EventsReleaserSchema(meta)
    else:
      return None


