class AIHandleQuestion():

  @classmethod
  def get_translate_q(cls,text):
    return '将英文翻译为中文，并保持原意: '+text
  
  @classmethod
  def get_translate_article_q(cls,article,rule):
    q_list = [
      '按如下要求将文章翻译为中文，并提供一个有吸引力的新闻标题',
      '1.文章长度不超过%s字，如果超出直接丢弃剩余段落' % rule.max_content_len,
      '2.标题长度不超过%s字' % rule.max_title_len,
      '3.英文字母和符号算0.5个字符',
      '4.如果文章开头有消息来源，移除它',
      '5.文章中所有消息来源都改为深蓝科技',
      '6.输出时不需要标题和翻译提示，只要把标题放在第一行即可',
      '文章如下',
    ]
    q = '，'.join(q_list)+'：'+article
    return q

  @classmethod
  def get_rewrite_q(cls,article,rule):
    '''
    param {str} article
    param {AIHandleRule} rule
    '''
    q_list = [
      '按如下要求重写文章',
      '1.文章长度不超过%s字' % rule.max_content_len,
      '2.采用夸张演绎手法',
      '3.与原文相似度低于百分之二十',
      '4.提供一个夸张风格标题',
      '5.标题长度不超过%s字' % rule.max_title_len,
      '6.英文字母和符号算0.5个字符',
      '文章如下',
    ]
    q = '，'.join(q_list)+'：'+article
    return q

  @classmethod
  def get_comment_q(cls,article,rule):
    '''
    param {str} article
    param {AIHandleRule} rule
    '''
    q_list = [
      '按如下要求发表评论',      
      '1.评论长度不超过%s字' % rule.max_content_len,
      '2.使用积极、乐观、赞美的语气',
      '3.评论前先用一句话总结新闻（包括时间）',
      '3.每个段落长度不要超过200字',
      '4.提供一个时髦的有吸引力的评论标题',
      '5.标题长度不超过%s字' % rule.max_title_len,
      '6.英文字母和符号算0.5个字符',
      '文章如下',
    ]
    q = '，'.join(q_list)+'：'+article
    return q

  @classmethod
  def get_comment_q_2(cls,article,rule):
    '''
    param {str} article
    param {AIHandleRule} rule
    '''
    q_list = [
      '按如下要求发表评论',      
      '1.评论长度不超过%s字' % rule.max_content_len,
      '2.使用阴阳怪、冷嘲热讽、负能量的语气',
      '3.评论前先用一句话总结新闻（包括时间）',
      '3.每个段落长度不要超过200字',
      '4.提供一个评论标题',
      '5.标题长度不超过%s字' % rule.max_title_len,
      '6.英文字母和符号算0.5个字符',
      '文章如下',
    ]
    q = '，'.join(q_list)+'：'+article
    return q