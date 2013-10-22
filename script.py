#!/usr/bin/env python

import os
import hashlib
import sys

class MerkleTree:
	def __init__(self, root):
		self._linelength = 50
		self._root = root
		self._mt = {}
		self._hashlist = {}
		self._tophash = ''
		self.__MT__()
		
	def Line(self):
		print self._linelength * '-'
				
	def MT(self):
		for node, hash in self._hashlist.iteritems():
			items = self.GetItems(node)
			value = []
			value.append(node)
			list = {}
			for item in items:
				if node == self._root:
					list[self._hashlist[item]] = item
				else:
					list[self._hashlist[os.path.join(node, item)]] = os.path.join(node, item)
			value.append(list)
			self._mt[hash] = value
		self._tophash = self._hashlist[self._root]

	def PrintHashList(self):
		self.Line()
		for item, itemhash in slef._hashlist.iteritems():
			print "%s %s" % (itemhash, item)
		self.Line()
		return
	
	def PrintMT(self, hash):
		value = self._mt[hash]
		item = value[0]
		child = value[1]
		print "%s %s" % (hash, item)
		if not child:
			return 
		for itemhash, item in child.iteritems():
			print "      -> %s %s" % (itemhash, item)
		for itemhash, item in child.iteritems():
			self.PrintMT(itemhash)
		
	def __MT__(self):
		self.HashList(self._root)
#		self.PrintHashList()
		self.MT()
		print "Merkle Tree for %s: " % self._root
		self.PrintMT(self._tophash)
		self.Line()
		
	def md5sum(self, data):
		m = hashlib.md5()
		fn = os.path.join(self._root, data)
		if os.path.isfile(fn):
			try :
				f = file(fn, 'rb')
			except:
				return 'Error : Unable to open %s' % fn
			while True:
				d = f.read(8096)
				if not d:
					break
				m.update(d)
			f.close()
		else:
			m.update(data)
		return m.hexdigest()
						
	def GetItems(self, directory):
		value = []
		if directory != self._root:
			directory = os.path.join(self._root, directory)
		if os.path.isdir(directory):
			items = os.listdir(directory)
			for item in items:
				value.append(item)
			value.sort()
		return value 					 

	def HashList(self, rootdir):
		self.HashListChild(rootdir)
		items = self.GetItems(rootdir)
		if not items:
			self._hashlist[rootdir] = ''
			return
		s = ''
		for subitem in items:
			s = s + self._hashlist[subitem]
		self._hashlist[rootdir] = self.md5sum(s)
		
	def HashListChild(self, rootdir):
		items = self.GetItems(rootdir)
		if not items:
			self._hashlist[rootdir] = ''
			return
		for item in items:
			itemname = os.path.join(rootdir, item)
			if os.path.isdir(itemname):
				self.HashListChild(item)
				subitems = self.GetItems(item)
				s = ''
				for subitem in subitems:
					s = s + self._hashlist[os.path.join(item, subitem)]
				if rootdir == self._root:
					self._hashlist[item] = self.md5sum(s)
				else:
					self._hashlist[itemname] = self.md5sum(s)
			else:
				if rootdir == self._root:
					self._hashlist[item] = self.md5sum(item)
				else:
					self._hashlist[itemname] = self.md5sum(itemname)
					
					
# this function used to calcute the difference between the two merkle trees

def MTDiff(mt_a, a_tophash, mt_b, b_tophash):
	if a_tophash == b_tophash:
		print "Top hash is equal for %s and %s" % (mt_a._root, mt_b._root)	# do nothing
	else:		# if top hashes are not same, synchronization process by comparing hashes and transfering only the data which has been changed.
		a_value = mt_a._mt[a_tophash]
		a_child = a_value[1] 	# retrieve the child list for merkle tree a
		b_value = mt_b._mt[b_tophash]
		b_child = b_value[1] 	# retrieve the child list for merkle tree b
		
		for itemhash, item in a_child.iteritems():
			try:
				if b_child[itemhash] == item:
					print "Information same : %s" % item
			except:
				print "Information Different : %s" % item
				temp_value = mt_a._mt[itemhash]
				if len(temp_value[1]) > 0:	# checks if this is a directory
					diffhash = list(set(b_child.keys()) - set(a_child.keys()))
					MTDiff(mt_a, itemhash, mt_b, diffhash[0])



if __name__ == "__main__":
	my_input1 = sys.argv[1]
	mt_a = MerkleTree(my_input1)
#	print mt_a._mt
#	my_input2 = sys.argv[2]
#	mt_b = MerkleTree(my_input2)
#	MTDiff(mt_a, mt_a._tophash, mt_b, mt_b._tophash)
	
	
