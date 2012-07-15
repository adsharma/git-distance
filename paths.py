#!/usr/bin/env python

""" 
Analyze the output of:
git log --pretty="format:%an : %cn :  %h : %p" v2.6.32.. > commit-paths.txt
"""

import sys, string

class AutoVivificationL(dict):
    """Return an empty list if not found"""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = []
            return value

class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

linus = "Linus Torvalds"
commits = AutoVivificationL()
children = AutoVivificationL()
authors = AutoVivification()

for line in open('commit-paths.txt'):
  author, committer, hash, parents = [string.strip(x) for x in line.split(':', 3)]
  commits[hash] = [author, committer, parents, -1]
  for parent in parents.split():
      children[parent].append(hash)

def search(child, committer, distance, depth):
  if depth > 10: return distance
  child = children[child]
  if len(child) == 0: return 11
  min_d = 11
  for c in child:
    new_committer = commits[c][1]
    if new_committer == linus:
      return distance+1
    inc = (new_committer != committer)
    d = search(c, new_committer, distance+inc, depth+1)
    if d < min_d: min_d = d
  return min_d

for commit, data in commits.items():
  author, committer, parents, distance = data
  if author == linus:
    distance = 0
  elif committer == linus:
    distance = 1
  else:
    distance = search(commit, committer, 1, 1)
  commits[commit] = [author, committer, parents, distance]
  if type(authors[author][distance]) == type(authors):
    authors[author][distance] = 1
  else:
    authors[author][distance] += 1
  
for author, data in authors.items():
  sum = 0
  n = 0
  for distance, num in data.items(): 
    if distance != 11:
      sum += distance * num
      n += num
  if n: 
    print n, sum * 1.0/n, author, data
