# -*- coding: iso-8859-1 -*-
import networkx as nx
from random_partition import RandomPartition
#import psyco

#psyco.full()
#psyco.log()

class PartitionAnalyzer (object):
  """A class implementing a partition analyzer.
     To check if the partition is regular or open according to the given set, it creates a graph with the following rules:
       - partition blocks become graph nodes; 
       - edges between blocks A and B exists if there's a relation between at least one element of block A and one element of block B.
     Then:
       - the partition is regular if the related graph is acyclical;
       - the partition is open if, for each element e of the poset, the filter of the element e is equal to the unions of the blocks that contains the elements of the same filter.
  """
  def __init__(self, poset, partition):
    '''Initialize a PartitionAnalyzer from 
       - a Poset object, or a string representing a poset (ex. ["a","b", "c","d"]) 
       - a RandomPartition object, or a string representing a partition (ex. [set(a,b), set(c), set(d)])
    '''
    if partition.__class__ == RandomPartition:
      self.partition_elements = partition.blocks.values()
    else:
      self.partition_elements = partition
    
    # create a graph. It will be used to check partition properties according to the given poset
    self.graph = nx.DiGraph()
    # partition blocks become graph nodes
    for i in range(len(self.partition_elements)):
      self.graph.add_node(i)

    if poset.__class__ == Poset:
      self.poset = poset
      # poset relations become edges between graph nodes
      for edge in poset.edges():
	from_v, to_v = edge
	for x in self.partition_elements:
	    if from_v in x:
	      from_v = self.partition_elements.index(x)
	    if to_v in x:
	      to_v = self.partition_elements.index(x)
	#TODO se from_v e to_v sono definiti, esci dal ciclo
	if from_v == to_v:
	  continue
	self.graph.add_edge(from_v, to_v)
    else:
      # create Poset object from poset string
      poset_edges = []
      for i in xrange(0,len(poset),2):
	if poset[i] != poset[i+1]:
	  poset_edges.append([poset[i], poset[i+1]])
      self.poset = Poset(poset_edges)
	  
      i = 0
      # poset relations become edges between graph nodes
      for i in xrange(0,len(poset),2):
	for x in self.partition_elements:
	  if poset[i] in x:
	    from_v = self.partition_elements.index(x)
	  if poset[i+1] in x:
	    to_v = self.partition_elements.index(x)
	  #TODO se from_v e to_v sono definiti, esci dal ciclo
	if from_v == to_v:
	  continue
	self.graph.add_edge(from_v, to_v)
    
  def check_if_regular(self):
    """check if the partition is regular according to the given poset."""
    return nx.is_directed_acyclic_graph(self.graph)

  def check_if_open(self):
    """check if the partition is open according to the given poset."""
    for block in self.graph.nodes():
      # let's build the union of the filters of every node in the current block
      filtro = set()
      for vertex in self.partition_elements[block]:
  	filtro = filtro.union(set(nx.dfs_preorder(self.poset, source = vertex)))
      blocks_union = set()
      # let's build the union of the blocks containing at least one node of the filter
      for vertex in filtro:
	for block in self.partition_elements:
	  if vertex in block:
	    blocks_union = blocks_union.union(block)
	    break
      # let's check if they are the same set, or not
      if filtro != blocks_union:
	return False
    return True

class Poset (nx.DiGraph):
  "A class implementing a poset as a graph."
  def __init__(self, edges):
    nx.DiGraph.__init__(self, edges, weighted=False)