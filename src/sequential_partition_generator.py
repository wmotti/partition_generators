#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
from cache import FactCache, BinomCache, BellCache
from sequential_partition import SequentialPartition
#import psyco

#psyco.full()
#psyco.log()

class SequentialPartitionGenerator (object):
  "A class that generate all the partitions of a set and analyze them."
     
  def __init__(self, poset = ["a","b", "c","d"], check = True, print_stats = True, pbar = True):
    """Parameters:
       - poset: a representation of the poset
       - check: if true, check for for partitions' properties (regularity and openness)
       - print_stats: print statistics about partitions at the end of the computation
       - pbar: show a progress bar during the computation
    """
    if pbar:
      try:
	import progressbar
      except ImportError:
	print "[warning] the progressbar module cannot be found. No progress bar will be shown."
	pbar = False
	pass
      else:
	widgets = ['Generating partitions: ', progressbar.Percentage(), ' ', progressbar.Bar('#'),' ', progressbar.ETA()]
    if check:
      try: 
	from partition_analyzer import PartitionAnalyzer, Poset
      except ImportError:
	print "[warning] the partition_analyzer module cannot be found. Partitions properties won't be checked."
	check = False
	pass
    elements_set = list(set(poset))
    self.elements_set_size = len(elements_set)
    self.print_stats = print_stats
    self.fact_cache = FactCache(self.elements_set_size)
    self.binom_cache = BinomCache(self.fact_cache)
    self.bell_cache = BellCache(self.binom_cache)
    if pbar:
      self.pbar = progressbar.ProgressBar(widgets=widgets,maxval=self.bell_cache.get(self.elements_set_size)).start()
    if check:
      # initialize structures for checking partitions' properties
      poset_edges = []
      self.regular_partitions = []
      self.open_partitions = []
      for i in xrange(0,len(poset),2):
	if poset[i] != poset[i+1]:
	  poset_edges.append([poset[i], poset[i+1]])
      self.poset = Poset(poset_edges)
      self.counter_regular_partitions = 0
      self.counter_open_partitions = 0
    sp = SequentialPartition(elements_set)
    gen = sp.gen()
    i = 0
    while True:
      try:
	cur_partition = gen.next()
	i += 1
      	if pbar:
	  self.pbar.update(i)
	if check:
	  pa = PartitionAnalyzer(self.poset, cur_partition)
	  if pa.check_if_regular():
	    self.counter_regular_partitions += 1
	    self.regular_partitions.append(cur_partition)
	  if pa.check_if_open():
	    self.counter_open_partitions += 1
	    self.open_partitions.append(cur_partition)
      except StopIteration:
	break
    if pbar:
      self.pbar.finish()
    if check == True:
      self.stats()

    del(self.fact_cache)
    del(self.binom_cache)
    del(self.bell_cache)

  def stats(self):
    "Computes partitions' statistics and print them (if requested)"
    #partizioni = self.partitions.keys()
    self.partizioni_generate = self.bell_cache.get(self.elements_set_size)
    self.partizioni_regolari = self.counter_regular_partitions
    self.partizioni_aperte = self.counter_open_partitions 
    if self.print_stats == True:
      print "Partizioni generate:            ", self.partizioni_generate
      print "Partizioni regolari:            ", self.partizioni_regolari
      print "Partizioni aperte:              ", self.partizioni_aperte



if __name__ == "__main__":
  poset_string = raw_input("Poset: ")
  pss = poset_string.split('"')
  if len(pss) == 1:
    pss = poset_string.split("'")
  poset = []
  for i in xrange(1,len(pss),2):
    poset.append(pss[i])

  positive_input = ['', 'S', 's', 'Y', 'y']
  negative_input = ['N', 'n']
  valid_input = positive_input + negative_input

  check = raw_input("Verifica le proprietà delle partizioni (S/n): ")
  while not check in valid_input:
    check = raw_input("Tasto non corretto, riprova: ")
  if check in positive_input:
    check = True
  else:
    check = False

  print_stats = raw_input("Stampa le statistiche conclusive (S/n): ")
  while not print_stats in valid_input:
    print_stats = raw_input("Tasto non corretto, riprova: ")
  if print_stats in positive_input:
    print_stats = True
  else:
    print_stats = False

  pbar = raw_input("Stampa una barra di avanzamento (S/n): ")
  while not pbar in valid_input:
    pbar = raw_input("Tasto non corretto, riprova: ")
  if pbar in positive_input:
    pbar = True
  else:
    pbar = False

  spg = SequentialPartitionGenerator(poset, check, print_stats, pbar)