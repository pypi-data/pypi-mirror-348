import sys,os,re
from .Publisher import Publisher

class OnceLoginPublisher(Publisher):

  def login(self):
    self.browser = self.loginer.login()
    if not self.browser:
      BluesConsole.error('Login failure')
      raise Exception('Login failure')