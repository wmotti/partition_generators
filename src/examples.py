#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

from random_partition_generator import RandomPartitionGenerator as RPG
rpg = RPG(1000)
rpg = RPG(10000)
rpg = RPG(100000)
rpg = RPG(100000,poset = ["a","b", "a","d", "d","c", "d","e"])
rpg = RPG(100000,poset = ["a","b", "a","d", "d","c", "d","e", "f","g"])
rpg = RPG(100000,poset = ["a","b", "a","d", "c","e", "f","g"])
rpg = RPG(100000,poset = ["a","b", "a","d", "c","e", "f","g", "h","b", "i","b", "j","i", "k","e"])
rpg = RPG(1000000,poset = ["a","b", "a","d", "c","e", "f","g", "h","b", "i","b", "j","i", "k","e"])


from sequential_partition_generator import SequentialPartitionGenerator as SPG
spg = SPG()
spg = SPG(poset = ["a","b", "a","d", "d","c", "d","e"])
spg = SPG(poset = ["a","b", "a","d", "d","c", "d","e", "f","g"])
spg = SPG(poset = ["a","b", "a","d", "c","e", "f","g"])
spg = SPG(poset = ["a","b", "a","d", "c","e", "f","g", "h","b", "i","b", "j","i", "k","e"])
