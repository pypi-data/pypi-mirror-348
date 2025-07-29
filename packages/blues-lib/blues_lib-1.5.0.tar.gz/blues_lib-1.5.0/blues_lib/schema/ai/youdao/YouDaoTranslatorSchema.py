import sys,os,re,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.ai.AIQASchema import AIQASchema

class YouDaoTranslatorSchema(AIQASchema):

  def create_url_atom(self):
    self.url_atom = self.atom_factory.createURL('QA page url','https://fanyi.youdao.com/#/TextTranslate')

  def create_question_atom(self):
    atoms = [
      self.atom_factory.createInput('input','#js_fanyi_input','${question}'),
    ]

    self.question_atom = self.atom_factory.createArray('question',atoms)

  def create_submit_atom(self):
    # don't need submit manually
    pass

  def create_answer_atom(self):
    atoms = [
      self.atom_factory.createJSCss('popout','.ai-guide',{
        'display':'none',
      }),
      self.atom_factory.createPause('wait to answer',5),
      # click a element before click the copy button, or it always copy failure
      self.atom_factory.createClickable('input','#js_fanyi_input'),
      self.atom_factory.createPause('pause',1),
      # must use js click or always copy failure
      self.atom_factory.createJSClickable('copy','.target .ic_translate_copy'),
    ] 
    self.answer_atom = self.atom_factory.createArray('wait and copy',atoms)
    