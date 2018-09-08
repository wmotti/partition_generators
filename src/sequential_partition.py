# -*- coding: iso-8859-1 -*-

class SequentialPartition (object):
  """A generator for partitions of a given set.
     It uses an algorithm described in "Combinatorial Algorithms" (II ed.) by Nijenhuis and Wilf, Academic Press, 1978, pages 88-92.
  """
  
  def __init__(self, elements_set = ['a','b','c','d']):
    """Constructor of the class.
       Parameters: 
	 - elements_set: an array of elements
    """
    self.elements_set = elements_set
    self.gen()

  def gen(self):
    "The algorithm to generate partitions' sequence."
    # p[i] is the numbers of elements in the class i
    p = {}
    # q[j] is the class which element j belongs to
    q = {}
    # n is the number of the elements
    n = len(self.elements_set)
    # nc is the number of the classes
    nc = 1
    p[1] = n
    for i in xrange(n):
      q[i+1] = 1
    # now all the elements are in a single class: this is the first partition
    while True:
      yield self.to_array(q)
      # now we iterate over all the other partitions
      # tille every element is alone in a class
      if nc != n:
	# m is the active letter (the one that change class)
        m = n
        l = q[m]
        while p[l] == 1:
          q[m] = 1
          m -= 1
          l = q[m]
        nc += m - n
        p[1] += n - m
        if l == nc:
          nc += 1
          p[nc] = 0
	# m is moved in a new class
        q[m] = l+1
        p[l] -= 1
        p[l+1] += 1
      else:
        break
    return

  def to_array(self,q):
    partition = {}
    for b in xrange(max(q.values())):
      partition[b+1] = set()
    for element in q:
      partition[q[element]].add(self.elements_set[element-1])
    return partition.values()