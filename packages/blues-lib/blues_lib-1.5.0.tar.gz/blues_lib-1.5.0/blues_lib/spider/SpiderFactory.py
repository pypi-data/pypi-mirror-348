import sys,re,os
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from spider.BriefsSpider import BriefsSpider
from spider.MaterialSpider import MaterialSpider
from spider.MaterialsSpider import MaterialsSpider
from spider.grid.GridBriefSpider import GridBriefSpider
from spider.grid.GridMaterialSpider import GridMaterialSpider

class SpiderFactory:

  def __init__(self,request):
    self._request = request

  def create_briefs(self):
    return BriefsSpider(self._request)

  def create_material(self):
    return MaterialSpider(self._request)

  def create_materials(self):
    return MaterialsSpider(self._request)

  def create_grid_brief(self):
    return GridBriefSpider(self._request)

  def create_grid_material(self):
    return GridMaterialSpider(self._request)