from .BriefsCrawler import BriefsCrawler
from .MaterialCrawler import MaterialCrawler
from .MaterialsCrawler import MaterialsCrawler
from .grid.GridBriefCrawler import GridBriefCrawler
from .grid.GridMaterialCrawler import GridMaterialCrawler

class CrawlerFactory:

  def __init__(self,request:dict):
    self._request = request

  def create_briefs(self):
    return BriefsCrawler(self._request)

  def create_material(self):
    return MaterialCrawler(self._request)

  def create_materials(self):
    return MaterialsCrawler(self._request)

  def create_grid_brief(self):
    return GridBriefCrawler(self._request)

  def create_grid_material(self):
    return GridMaterialCrawler(self._request)
  