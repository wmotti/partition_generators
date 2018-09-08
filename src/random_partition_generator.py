#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
from __future__ import division
from cache import FactCache, BinomCache, BellCache, ProbClassSizeCache
from random_partition import RandomPartition
#import psyco

#psyco.full()
#psyco.log()

class RandomPartitionGenerator (object):
  "A class that generates uniform random partitions and analyze them."
  def __init__(self, n, poset = ["a","b", "c","d"], check = True, print_stats = True, pbar = True):
    """Parameters:
       - n: number of partitions to be created
       - poset: a representation of the poset
       - check: if true, check for for partitions' properties (regularity and openness)
       - print_stats: print statistics about partitions at the end of the computation
       - pbar: show a progress bar during the computation
    """
    if pbar:
      try:
	import progressbar
      except ImportError:
	print "warning: the progressbar module cannot be found. No progress bar will be shown."
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
    self.n = n
    self.print_stats = print_stats
    if pbar:
      self.pbar = progressbar.ProgressBar(widgets=widgets,maxval=n).start()
    self.partitions = {}
    self.fact_cache = FactCache(self.elements_set_size)
    self.binom_cache = BinomCache(self.fact_cache)
    self.bell_cache = BellCache(self.binom_cache)
    self.prob_cache = ProbClassSizeCache(self.binom_cache, self.bell_cache)
    self.distinct_partitions = 0
    if check:
      # initialize structures for checking partitions' properties
      poset_edges = []
      self.regular_partitions = []
      self.open_partitions = []
      for i in range(0,len(poset),2):
	if poset[i] != poset[i+1]:
	  poset_edges.append([poset[i], poset[i+1]])
      self.poset = Poset(poset_edges)
      self.counter_regular_partitions = 0
      self.counter_open_partitions = 0
      self.counter_partitions_sampled = 0
    while self.distinct_partitions < n:
      if check and self.distinct_partitions == self.bell_cache.get(self.elements_set_size):
	break
      rup = RandomPartition(elements_set, fact_cache = self.fact_cache, binom_cache = self.binom_cache, prob_cache = self.prob_cache)
      self.counter_partitions_sampled += 1
      rp = rup.partition_string()
      if rp in self.partitions:
	already_known = True
	self.partitions[rp] += 1
      else:
	already_known = False
	self.partitions[rp] = 1
	self.distinct_partitions += 1
	if pbar:
	  self.pbar.update(self.distinct_partitions)
      if check and not already_known:
	pa = PartitionAnalyzer(self.poset, rup)
	if pa.check_if_regular():
	  self.counter_regular_partitions += 1
	  self.regular_partitions.append(rp)
	if pa.check_if_open():
	  self.counter_open_partitions += 1
	  self.open_partitions.append(rp)
    if pbar:
      self.pbar.finish()
    if check == True:
      self.stats()

    self.fact_cache.pickle_data()
    self.binom_cache.pickle_data()
    self.bell_cache.pickle_data()
    self.prob_cache.pickle_data()

  def stats(self):
    "Compute partitions' statistics and print them (if requested)"
    partizioni = self.partitions.keys()
    varianza_camp = 0
    #print partizioni
    # calcola la media campionaria 
    media_camp = self.counter_partitions_sampled / self.distinct_partitions
    # calcola la varianza campionaria 
    for x in self.partitions.values():
      varianza_camp += (x-(media_camp))**2
    varianza_camp = varianza_camp / (self.counter_partitions_sampled-1)
    self.partizioni_richieste = self.n
    self.partizioni_campionate = self.counter_partitions_sampled
    self.partizioni_campionate_percentuale = self.counter_partitions_sampled / self.n * 100
    self.partizioni_distinte_note = self.bell_cache.get(self.elements_set_size)
    self.partizioni_distinte_note_percentuale = self.distinct_partitions / self.counter_partitions_sampled * 100
    self.partizioni_distinte_campionate = self.distinct_partitions
    self.partizioni_distinte_campionate_percentuale = self.distinct_partitions / self.bell_cache.get(self.elements_set_size) * 100
    self.partizioni_regolari = self.counter_regular_partitions
    self.partizioni_regolari_percentuale = self.counter_regular_partitions / self.distinct_partitions * 100
    self.partizioni_regolari_stimate = self.counter_regular_partitions  / (self.distinct_partitions / self.bell_cache.get(self.elements_set_size))
    self.partizioni_aperte = self.counter_open_partitions 
    self.partizioni_aperte_percentuale = self.counter_open_partitions / self.distinct_partitions * 100
    self.partizioni_aperte_stimate = self.counter_open_partitions / (self.distinct_partitions / self.bell_cache.get(self.elements_set_size))
    if self.print_stats == True:
      print "Partizioni richieste:           ", self.partizioni_richieste
      print "Partizioni campionate:          ", self.partizioni_campionate, "("+str(self.partizioni_campionate_percentuale)+"%)" 
      print "Partizioni distinte note:       ", self.partizioni_distinte_note, "("+str(self.partizioni_distinte_note_percentuale)+"%)" 
      print "Partizioni distinte campionate: ",self.partizioni_distinte_campionate , "("+str(self.partizioni_distinte_campionate_percentuale)+"%)"
      print "Media campionaria:              ", media_camp
      print "Varianza campionaria:           ", varianza_camp
      print "Partizioni regolari:            ", self.partizioni_regolari, "("+str(self.partizioni_regolari_percentuale)+"%)" 
      print "Partizioni regolari stimate:    ", self.partizioni_regolari_stimate
      print "Partizioni aperte:              ", self.partizioni_aperte, "("+str(self.partizioni_aperte_percentuale)+"%)"
      print "Partizioni aperte stimate:      ", self.partizioni_aperte_stimate



if __name__ == "__main__":
  n = int(raw_input("Numero di partizioni da generare: "))

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

  rpg = RandomPartitionGenerator(n, poset, check, print_stats, pbar)
