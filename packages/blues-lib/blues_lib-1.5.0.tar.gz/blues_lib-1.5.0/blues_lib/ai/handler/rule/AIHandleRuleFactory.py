from .AIHandleRule import AIHandleRule
from .AITextHandleRule import AITextHandleRule

class AIHandleRuleFactory():
  
  @classmethod
  def create(cls,scenario=''):
    if scenario == 'rewrite':
      return AITextHandleRule(max_title_len=28,min_title_len=5,max_content_len=500,min_content_len=150,max_retry_count=3)
    elif scenario == 'comment':
      return AITextHandleRule(max_title_len=28,min_title_len=5,max_content_len=400,min_content_len=150,max_retry_count=3)
    elif scenario == 'translate':
      return AIHandleRule(min_text_len=1,max_retry_count=3)
    elif scenario == 'translate_article':
      return AITextHandleRule(max_title_len=28,min_title_len=5,max_content_len=5000,min_content_len=150,max_retry_count=3)
    else:
      return AIHandleRule()
