import yummly
from yummly import Client
from collections import Counter
from sets import Set

class SearchResults(object):

  def __init__(self, matches):
    self.matches = matches
    self.num_matches = len(matches)
    self.cnt = Counter()
    self.ingredset_by_recipe = dict()
    self.intensity_by_flavor = Counter()
    self.images = []
    self.avg_time = 0.0
    self.photos = []
    self.parse()

  def parse(self):
    time = 0
    num_matches = len(self.matches)
    for match in self.matches:
      self.ingredset_by_recipe[match.id] = match.ingredients
      for i in match.ingredients:
        self.cnt[i.encode('utf-8').strip()]+=1
      flavors = ['salty', 'meaty', 'piquant', 'bitter', 'sour', 'sweet']
      #need to track simple distribution
      for flavor in flavors:
          try:
            self.intensity_by_flavor[flavor] += match.flavors[flavor]
            flavor_count+=1
          except:
            pass
      if match.smallImageUrls:
        self.photos.extend(match.smallImageUrls)
      if match.totalTimeInSeconds:
        time += match.totalTimeInSeconds
    self.avg_time = (time/num_matches)/60

  def core_ingredients(self):
    return [i[0].encode('utf-8').strip() for i in self.cnt.most_common(10)]

class YummlyClient(object):

  TIMEOUT = 5.0
  RETRIES = 0

  def __init__(self, api_id, api_key):
    self.client = Client(api_id=api_id, api_key=api_key, timeout=self.TIMEOUT, retries=self.RETRIES)

  def find_consensus(self, query):
    results = SearchResults(self.client.search(query).matches)
    return results.core_ingredients(), results
