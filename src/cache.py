# -*- coding: iso-8859-1 -*-
from __future__ import division
import pickle

class LookupTable (object):
  "A class implementing a simple lookup table."

  def __init__(self, func):
    """Constructor of the class.
       Parameter:
         - func: a function defining how new values (not in the table) are calculated
    """
    self.data = {}
    self.func = func
 
  def pickle_data(self, cache_file):
    f = open(cache_file, 'wb')
    pickle.dump(self.data, f)
    f.close()

  def set(self, a, b):
    "Set location (a,b) with value self.func(a,b)."
    if not a in self.data:
      self.data[a] = {}
    v = self.func(a, b)
    self.data[a][b] = v
    return v

  def get(self, a, b):
    "Get value from location (a,b). If missing, it is computed and stored too."
    try: 
      return self.data[a][b]
    except (KeyError, IndexError):
      return self.set(a, b)

class FactCache (object):
  "A class implementing a lookup table per factorial values."

  def __init__(self, n):
    """Constructor of the class.
       Parameter: 
         - n: during initialization, fact(1), ..., fact(n) are computed
    """
    self.data = []
    try:
      f = open('fact_cache.pkl', 'rb')
    except IOError:
      # fact(0) = 1
      self.data.append(1)
      for i in range(n):
	# fact(n) = fact(n-1) * n
	self.data.append(self.data[i]*(i+1))
    else:
      self.data = pickle.load(f)

  def pickle_data(self):
    f = open('fact_cache.pkl', 'wb')
    pickle.dump(self.data, f)
    f.close()

  def get(self, n):
    """Returns factorial of n. 
       If missing from the cache, it computes and stores it too."""
    try:
      return self.data[n]
    except IndexError:
      return self.set(n)

  def set(self, n):
    "Computes factorial of n."
    for i in xrange(len(self.data), n+1):
      # fact(n) = fact(n-1) * n
      self.data.append(self.data[i-1]*i)
    return self.data[n]

class BinomCache (LookupTable):
  "A class implementing a lookup table for binomial values."
  
  def __init__(self, fact_cache):
    """Constructor of the class.
       Parameter:
         - fact_cache: an instance of FactCache to be used during binomial computations
    """
    LookupTable.__init__(self, self.func)
    try:
      f = open('binom_cache.pkl', 'rb')
    except IOError:
      pass
    else:
      self.data = pickle.load(f)
    self.fact_cache = fact_cache
    
  def pickle_data(self):
    LookupTable.pickle_data(self, 'binom_cache.pkl')

  def func(self, a, b):
    "The function that computes the binomial of a and b"
    fact_a = self.fact_cache.get(a)
    fact_b = self.fact_cache.get(b)
    fact_a_minus_b = self.fact_cache.get(a-b)
    return fact_a // (fact_b * fact_a_minus_b) # divisione intera

class BellCache (object):
  "A class implementing a lookup table for Bell numbers."
  
  def __init__(self, binom_cache):
    """Constructor of the class.
       Parameter:
         - binom_cache: an instance of BinomCache to be used during Bell numbers' computations
    """
    try:
      f = open('bell_cache.pkl', 'rb')
    except IOError:
      self.data = [1, 1, 2, 5, 15, 52, 203, 877, 4140, 21147, 115975, 
	    678570, 4213597, 27644437, 190899322, 1382958545, 
	    10480142147, 82864869804, 682076806159, 5832742205057,
	    51724158235372, 474869816156751, 4506715738447323]
      #pass
    else:
      self.data = pickle.load(f)
    self.binom_cache = binom_cache

  def pickle_data(self):
    f = open('bell_cache.pkl', 'wb')
    pickle.dump(self.data, f)
    f.close()

  def get(self, n):
    """Returns the Bell_n number.
       If missing from the cache, it computes and stores it too."""
    try:
      return self.data[n]
    except IndexError:
      return self.set(n)
   
  def set(self, n):
    "Computes the Bell_n number"
    for i in xrange(len(self.data), n+1):
      bell_n = 0
      for j in xrange(len(self.data)):
        bell_n += self.binom_cache.get(i-1, j) * self.data[j]
      self.data.append(bell_n)
    return self.data[n]

class ProbClassSizeCache (LookupTable):
  "A class implementing a lookup table per probability values."

  def __init__(self, binom_cache, bell_cache):
    """Constructor of the class.
       Parameter:
         - binom_cache: an instance of BinomCache to be used during probabilities computations
         - bell_cache : an instance of BellCache to be used during probabilities computations
    """
    LookupTable.__init__(self, self.func)

    try:
      f = open('prob_cache.pkl', 'rb')
    except IOError:
      pass
    else:
      self.data = pickle.load(f)
    self.binom_cache = binom_cache
    self.bell_cache  = bell_cache 
  
  def func(self, n, k):
    "Computes the probability of a k-block_size in a partition of a n-elements set."
    return self.binom_cache.get(n-1, k-1) * self.bell_cache.get(n-k) / self.bell_cache.get(n)

  def pickle_data(self):
    LookupTable.pickle_data(self, 'prob_cache.pkl')

##### examples #####
#
# from cache import *
# fc = FactCache(10)
# binc = BinomCache(fc)
# bellc = BellCache(binc)
# pc = ProbClassSizeCache(binc, bellc)
