import sys,os,re,copy
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from atom.AtomFactory import AtomFactory

class AtomCreator():

  @classmethod 
  def create(cls,meta:dict):
    '''
    Convert any atom meta to the Atom Object
    @param {dict} meta: a valid meta dict (must has the attr of 'kind'), such as:
      {"kind":"url","title":"homepage","value":"https://baidu.com"} 
    '''
    meta_copy = copy.deepcopy(meta)
    return cls.__convert(meta_copy)

  @classmethod 
  def __convert(cls,meta):
    '''
    convert a specify meta to a Atom
    '''
    if not isinstance(meta,dict):
      return meta

    # deal the nest atom value
    kind = meta.get('kind')
    value = meta.get('value')
    if not kind:
      return meta

    if isinstance(value,list) or isinstance(value,tuple):
      for item_idx,item_val in enumerate(value):
        value[item_idx] = cls.__convert(item_val)
    elif isinstance(value,dict):
      for key,val in value.items():
        value[key] = cls.__convert(val)

    method = cls.__get_method(kind)
    del meta['kind']
    if method:
      return method(**meta)
    else:
      return meta

  @classmethod
  def __get_method(cls,kind):
    '''
    Get the factory's create method
      - the kind in method name has one or more Upper letters
      - 'data' -> 'createData'
      - 'url' -> 'createURL'
    '''
    prefix = 'create'
    upper_kind = kind.lower()
    factory = AtomFactory()
    n = len(upper_kind)

    # 遍历每个字符，逐步大写
    for i in range(n):
      # 将第 i 个字符大写
      upper_kind = upper_kind[:i] + upper_kind[i].upper() + upper_kind[i+1:]
      method_name = prefix+upper_kind
      # 检查对象是否有该方法
      if hasattr(factory, method_name):
        return getattr(factory, method_name)
    return None
