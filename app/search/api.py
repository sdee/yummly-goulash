import yummly
from yummly import Client
from collections import Counter
from sets import Set

class SearchResults(object):

  def __init__(self, matches):
    self.matches = matches
    self.cnt = Counter()
    self.ingredset_by_recipe = dict()
    self.ingredlines_by_recipe = dict() #ingredlines have quantity and food
    self.intensity_by_flavor = Counter()
    self.extract_flavors()
    self.extract_ingredients()

  def extract_flavors(self):
    flavor_count = 0 #default count for recipes without a flavor profile
    for match in self.matches:
      flavors = ['salty', 'meaty', 'piquant', 'bitter', 'sour', 'sweet']
      for flavor in flavors:
          try:
            self.intensity_by_flavor[flavor] += match.flavors[flavor]
            flavor_count+=1
          except:
            pass

  def extract_ingredients(self):
    for match in self.matches:
      self.ingredset_by_recipe[match.id] = match.ingredients
      for i in match.ingredients:
        self.cnt[i.encode('utf-8').strip()]+=1

  def core_ingredients(self):
    return [i[0].encode('utf-8').strip() for i in self.cnt.most_common(10)]

class YummlyClient(object):

  TIMEOUT = 5.0
  RETRIES = 0
  cnt = Counter()
  ingredset_by_recipe = dict()
  ingredlines_by_recipe = dict() #ingredlines have quantity and food
  intensity_by_flavor = Counter()

  def __init__(self, api_id, api_key):
    self.client = Client(api_id=api_id, api_key=api_key, timeout=self.TIMEOUT, retries=self.RETRIES)

  def find_consensus(self, query):
    results = SearchResults(self.client.search(query).matches)
    return results.core_ingredients()
