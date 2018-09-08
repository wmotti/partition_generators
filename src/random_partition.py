# -*- coding: iso-8859-1 -*-
from __future__ import division
import random
from cache import FactCache, BinomCache, BellCache, ProbClassSizeCache
#import psyco

#psyco.full()
#psyco.log()

class RandomPartition (object):
  "A class implementing a uniform random partition, and the algorithm to generate it."
  def __init__(self, elements_set = ["a","b","c","d"], **kparams):
    """Gets an elements set as input and returns a uniform random partition on it.
       Parameters:
         - elements_set: a list of elements of the set;
         - *_cache: an object implementing a lookup table for storing and retrieve factorial, binomial and probability values. If False, it will be created;
         - debug: if True, it will print verbosely during execution.
       It uses an algorithm described in "Combinatorial Algorithms" (II ed.) by Nijenhuis and Wilf, Academic Press, 1978, pages 93-98.
    """
    # update default values with values passed as arguments
    params = { 'fact_cache' : False, 
	       'binom_cache' : False, 
	       'prob_cache' : False, 
	       'bell_cache' : False,
	       'debug' : False }
    params.update(kparams)
    self.n = len(elements_set)
    
    # reuse an existing *_cache or create a new one
    if params.has_key('fact_cache') and params['fact_cache']:
      self.fact_cache = params['fact_cache'] 
    else:
      self.fact_cache = FactCache(self.n)
    if params.has_key('binom_cache') and params['binom_cache']:
      self.binom_cache = params['binom_cache'] 
    else:
      self.binom_cache = BinomCache(self.fact_cache)
    if params.has_key('bell_cache') and params['bell_cache']:
      self.bell_cache = params['bell_cache'] 
    else:
      self.bell_cache = BellCache(self.binom_cache)
    if params.has_key('prob_cache') and params['prob_cache']:
      self.prob_cache = params['prob_cache'] 
    else:
      self.prob_cache = ProbClassSizeCache(self.binom_cache, self.bell_cache)
    self.debug = params['debug']
    self.elements_set = elements_set
    self.partition = [0] * self.n
    self.blocks = {}
    self.l = 0
    
    # run the algorithm
    self.run()

  def choose_classes_size(self):
    "Returns a random class size according to computed probabilities."
    for k in range(self.n):
      self.prob_cache.get(self.n, k+1)
    p = random.random()
    v_cum = 0
    class_size = 0
    for k, v in self.prob_cache.data[self.n].items():
      v_cum += v
      if p <= v_cum:
	class_size = k
	break
    self.l += 1
    self.partition[self.n-class_size:self.n] = [self.l]*class_size
    self.n -= class_size

  def run(self):
    "Core routine for uniform random partition generation."
    while self.n != 0:
      self.choose_classes_size()
    random.shuffle(self.partition)
    for n in range(max(self.partition)):
      self.blocks[n+1] = set()
    i = 0
    for v in self.partition:
      self.blocks[v].add(self.elements_set[i])
      i += 1
  
  def partition_string(self):
    "Returns a string rappresentation of the partition."
    blocks = self.blocks.values()
    blocks.sort(self.cmp_set)
    string = ""
    for b in blocks:
      b = list(b)
      b.sort()
      string += "{"
      for s in b:
	string += s
	string += ','
      string = string.rstrip(',')
      string += "}"
    return string
    
  def cmp_set(self,a,b):
    "Defines how to compare two sets."
    if min(a) < min(b):
      return -1
    if min(a) == min(b):
      return 0
    if min(a) > min(b):
      return 1
