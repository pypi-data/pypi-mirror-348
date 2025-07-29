import json

class AIQAResponse:

  def __init__(self,title,content):
    # {str}
    self.title = title if title else ''
    # {list<str>}
    self.content = content if content else None
    
  def to_string(self):
    entity = {
      'title':self.title,
      'content':self.content,
    }
    return json.dumps(entity,ensure_ascii=False) 