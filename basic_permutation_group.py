"""
This module contains some basic permutation group algorithms, for:

-computing orbits and transversals,
-computing generators for a stabilizer, and
-reducing a generating set to an equivalent one of at most quadratic size.

Most important functions:

 Orbit		(computes orbit and transversal)
 Stabilizer	(computes generators for a stabilizer subgroup)

Use this with permutation objects generated by the module permv2.py
(Or your own permutation objects that support equivalent methods).
"""

# basic_permutation_group.py: based on fir/perm/basicpermutationgroup
#	uses permv2, reversed composition.
# 18-03-2015, Paul Bonsma


from permv2 import Permutation
from time import time

def Orbit(generators,el,returntransversal=False):
	"""
	<generators> should be a Python list of permutations (from permv2.py), which
	represent a generating set of a permutation group H.
	<el> is an element of the ground set (which should be from 0...n-1).

	This function returns the orbit <O> of <el> in group H, as a python list.

	If <returntransversal> = True, it also returns a transversal <U>, which is
	an equal length python list:
	For every index i, U[i] is a permutation from H that maps <el> to O[i].

	(The lists O and U are returned as a 2-tuple.)

	See the lecture slides for this algorithm in pseudocode, and an example.
	"""
	O=[el]
	if len(generators)==0:
		return O,None
	n=generators[0].n
	memberVec=[0]*n
	memberVec[el]=1
	if returntransversal:
		U=[Permutation(n)]
	ind=0
	while ind<len(O):
		el=O[ind]
		for P in generators:
			mapel=P[el]
			if not memberVec[mapel]:
				memberVec[mapel]=1
				O.append(mapel)
				if returntransversal:
					U.append(P*U[ind])
		ind+=1
	for el in O:
		memberVec[el]=0
	if returntransversal:
		return O,U
	else:
		return O

def SchreierGenerators(generators,el):
	"""
	(Mostly for internal use.)
	Given a generating set <generators> (a Python list containing permutations) that
	generate a group H, and an element <el> (from the ground set 0...n-1),
	this function returns a number of permutations that are in the <el>-stabilizer subgroup
	of H, which is in fact a generating set for this stabilizer subgroup.
	This may be a long list, which may even contain duplicates.
	"""
	O,U=Orbit(generators,el,True)
	SchrGen=[]
	for ind in range(len(O)):
		el=O[ind]
		for P in generators:
			mapel=O.index(P[el])
			newgen=-U[mapel]*P*U[ind]
			if not newgen.istrivial():
				SchrGen.append(newgen)
	return SchrGen


def FindNonTrivialOrbit(generators):
	"""
	Given a generating set <generators> (a Python list containing permutations),
	this function returns an element <el> with a nontrivial orbit in the group
	generated by <generators>, or <None> if no such element exists.
	(Useful for order computation / membership testing.)
	"""
	if generators==[]:
		return None
	n=generators[0].n
	for P in generators:
		for el in range(n):
			if P[el]!=el:
				return el

def Reduce(generators,wordy=0):
	"""
	Given a generating set <generators> (a Python list containing permutations) that
	generates a group H, this function returns a possibly smaller generating set for the
	same group H (but certainly not larger).
	The resulting generating set will contain less than n^2
	permutations, when the permutations are on n elements.
	(Set <wordy> =1 or 2 to see what is going on exactly.)
	"""
	if wordy>=1:
		print("  Reducing. Input length:",len(generators))
	if generators==[]:
		return generators
	n=generators[0].n
	outputgenerators=[]
	todo=generators
	while todo!=[]:
		el=FindNonTrivialOrbit(todo)
		if el==None:	# can happen if the input (erroneously) contains trivial permutations
			break
		if wordy>=2:
			print("    Next iteration: still to reduce:\n     ",todo)
			print("    Reducing for element",el)
		images=[None]*n
		todonext=[]
		for P in todo:
			if P[el]==el:
				todonext.append(P)
			elif images[P[el]]==None:
				if wordy>=2:
					print("      Keeping",P,"which maps",el,"to",P[el])
				outputgenerators.append(P)
				images[P[el]]=P
			else:
				Q=-images[P[el]]*P
				if wordy>=2:
					print("      Changing",P,"to",Q)
				if not Q.istrivial():
					todonext.append(Q)
		todo=todonext
	if wordy>=1:
		print("  Output length:",len(outputgenerators))
	return outputgenerators


def Stabilizer(generators,el):
	"""
	<generators> should be a python list containing permutations (from permv2.py),
	which is viewed as a generating set for a group H.
	<el> should be an element from 0...n-1 (the ground set for the permutations).

	This function returns a generating set for H_{el}, the stabilizer subgroup of H
	for element <el>. The generating set has size less than n^2.
	"""
	return Reduce(SchreierGenerators(generators,el),0)

def IsMember(generators: "list[Permutation]", f: "Permutation") -> "bool":
	"""
		Checks if the new permutation is in the span of the generator group
		:param generators: a group of permutations
		;param f: the permutation to check if in span of generators
		:returns: True if f is already in the generating set, else False
	"""

	# if generating set empty, return false
	if not generators:
		return False

	# size of graph and permutation
	n = generators[0].n

	# arbitrary element of V
	alpha = FindNonTrivialOrbit(generators) # should be an element of V, so alpha ??? [0, n-1]

	# orbit of element and also the transversals
	orbit, transversalGroup = Orbit(generators, alpha, True) # orbit of element alpha and its transversals

	# for each element in the orbit, check if f maps alpha to it, if so check if the composition of the inverse of
	# the transversal of beta with f is a stabilizer generated by the generators
	beta = f[alpha]
	if beta not in orbit:
		return False
	i = orbit.index(beta)
	transversal = transversalGroup[i]
	composition = -transversal*f
	if composition[alpha] == alpha:
		return True
	# for i in range(len(orbit)):
	# 	beta = orbit[i]
	# 	if f[alpha] == beta:
	# 		transversal = transversalGroup[i]
	# 		composition = -transversal*f
	# 		print()
	# 		if composition[alpha] == alpha:
	# 			return True
			# for perm in ExpandStabilizers(Stabilizer(generators, alpha)):
			# 	if composition == perm:
			# 		return True
	return False

def OrderGenerators(generators: "list[Permutation]") -> "int":
	"""
		Recursively calculates the order of a given generating set.
		:param generators:the given generating set
		:returns: the order of the generators
	"""
	# if only the trivial permutation is left, return 1
	if len(generators) == 1 and generators[0].istrivial():
		return 1
	# alpha = FindNonTrivialOrbit(generators)
	alphaLen = 0
	stack = []
	for i in range(generators[0].n):
		stack.append(i)
	while stack:
		el = stack.pop()
		orbit = Orbit(generators, el, False)
		if len(orbit) > alphaLen:
			alpha = el
			alphaLen = len(orbit)
		for el2 in orbit:
			if el2 in stack:
				stack.remove(el2)

	if alpha is not None:
		orbit = Orbit(generators, alpha, False)
		stabilizer = Stabilizer(generators, alpha)
		order_orbit = len(orbit)
		# once the stabilizer is empty, you have recursively calculated the
		# order of the stabilizer
		if len(stabilizer) == 0:
			return order_orbit
		else:
			return order_orbit * OrderGenerators(stabilizer)


# def ExpandStabilizers(generators: "list[permutation]") -> "list[permutation]":
# 	"""
# 		:returns: (all possible?) permutations created by the generating permutations given
# 	"""
# 	# keep track of which stabilizers I still have to go through, I have seen and the ones I have found
# 	stack = list()
# 	seen = set()
# 	result = list()
#
# 	# add each stabilizer to the stack
# 	for stabilizer in generators:
# 		stack.append(stabilizer)
#
# 	# while there are stabilizers to check
# 	while stack:
# 		x = stack.pop()
# 		unseen = True
#
# 		# if it has already been seen, do not add it, else add it
# 		if CyclesToTuple(x.cycles()) in seen:
# 			unseen = False
# 		if unseen:
# 			stack.append(x*x)
# 			seen.add(CyclesToTuple((x*x).cycles()))
# 			result.append(x*x)
#
# 		# for all other stabilizers in stack, create possible stabilizers and check if it has already been seen, if so
# 		# do not add, else add
# 		for y in stack:
# 			r = [x*y, y*x, -x*y, x*-y, -y*x, y*-x]
# 			for perm in r:
# 				unseen = True
# 				if CyclesToTuple(perm.cycles()) in seen:
# 					unseen = False
# 				if unseen:
# 					stack.append(perm)
# 					seen.add(CyclesToTuple(perm.cycles()))
# 					result.append(perm)
#
# 	# return all found stabilizers
# 	return result

def CyclesToTuple(cycles: "list[list[int]]") -> "tuple[tuple[int]]":
	"""
		Tuple cycles of permutation, to compare 2 easier
		:perm cycles: the cycles of a permutation
		:returns: a tuple of the cycles
	"""
	hashCycles = []
	for i in range(len(cycles)):
		hashCycles.append(tuple(cycles[i]))
	return tuple(hashCycles)

def OrderStabilizers(alpha, generators: "list[Permutation]") -> "int":
	"""
		:returns: the amount of stabilizers in all the possible permutations given the generating permutations
	"""
	orderStabilizers = 0
	# stabilizers = ExpandStabilizers(generators)

	stack = list()
	for perm in generators:
		stack.append(perm)
	seen = set()

	while stack:
		x = stack.pop()
		# if CyclesToTuple(x.cycles()) in seen:
		# 	stack.append(x * x)
		# 	seen.add(CyclesToTuple((x * x).cycles()))
		# 	orderStabilizers += 1
		for y in stack:
			r = [x*y, y*x, -x*y, x*-y, -y*x, y*-x, x*x]
			for perm in r:
				if CyclesToTuple(perm.cycles()) in seen:
					stack.append(perm)
					seen.add(CyclesToTuple(perm.cycles()))
					orderStabilizers += 1
	# for perm in stabilizers:
	# 	if perm[alpha] == alpha:
	# 		orderStabilizers += 1
	return orderStabilizers

if __name__ == "__main__":

	# testing it using the examples provided in the slides
	generators = [Permutation(6, [[0, 1, 2], [4, 5]]), Permutation(6, [[2, 3]])]
	startt = time()
	print("Order computation test: ", OrderGenerators(generators))
	endtt = time()
	print(endtt - startt)
	generators = [Permutation(6, [[0, 1, 2], [4, 5]]), Permutation(6, [[2, 3]])]
	f = Permutation(6, [[0, 2]])
	startt = time()
	print("Membership test: ", IsMember(generators, f))
	endtt = time()
	print(endtt - startt)
