from .PublishPlan import PublishPlan

class PublishPlanFactory():

  def create_baijia(self,excepted_quota=None):
    platform = 'baijia'
    limit_quota = {
      'events':15,
      'news':0,
    }
    default_excepted_quota = {
      'events':1,
      'news':0,
    }
    actual_excepted_quota = excepted_quota if excepted_quota else default_excepted_quota

    return PublishPlan(platform,actual_excepted_quota,limit_quota)

  def create_toutiao(self,excepted_quota=None):
    platform = 'toutiao'
    limit_quota = {
      'events':10,
      'news':0,
    }
    default_excepted_quota = {
      'events':1,
      'news':0,
    }
    actual_excepted_quota = excepted_quota if excepted_quota else default_excepted_quota

    return PublishPlan(platform,actual_excepted_quota,limit_quota)
