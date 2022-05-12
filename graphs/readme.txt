This zip file contains two more zip files:

basic.zip is password protected and contains 6 instances to solve with a graph isomorphism algorithm.
pw=35%GnATja&
basicGI1.grl
basicGI2.grl
basicGI3.grl
basicGIAut1.grl
basicAut1.gr
basicAut2.gr

bonus.zip is itself not password protected, but contains 10 more password protected zip files. Each zip file contains a bonus instance file (each good for .1 bonus point if solved within the time limit).
pw=67$hok343ll
zip file:		contains:		pw:
bonusAut1.zip		bonusAut1.gr  		7113^6zBBf
bonusAut2.zip		bonusAut2.gr		ehMK5Q%9bw
bonusAut3.zip		bonusAut3.grl		*^U3BWoq05
bonusAut4.zip		bonusAut4.grl		t96u0#Ce75
bonusAut5.zip		bonusAut5.grl		d5Y9bQH9c&
bonusGI1.zip		bonusGI1.grl		8xV0CKou!H
bonusGI2.zip		bonusGI2.grl		@V3Kz@ha1k
bonusGI3.zip		bonusGI3.grl		cjk7gTT5&8
bonusGI4.zip		bonusGI4.grl		uBmC#J5N38
bonusGI5.zip		bonusGI5.grl		z&*2ZP5z7t


*GI*.grl files contain a list of graphs. The output should be a list of the equivalence classes of those graphs. I.e., sets of graphs that are isomorphic. The output may look something like

equivalence classes:
[0]
[1,2]
[3,4,5]
[6,7,8,9]

*GIAut*.grl files contain a list of graphs. The output should be a list of the equivalence classes of those graphs and the number of automorphisms that they have. The output may look something like

Automorphisms:
0:  1234
1:  12
2:  234
3:  12
4:  1234
5:  234

equivalence classes:
[0,4]
[1,3]
[2,5]

or

equivalence classes - automorphisms:
[0,4]: 	1234
[1,3]:  12
[2,5]:  234

*Aut*.gr files contain a single graph and *Aut*.grl files contain a list of graphs. The output should be a list of automorphisms that they have. The output may look something like

Automorphisms:
0:  1234
1:  12
2:  234
3:  12
4:  1234
5:  234

or, in case of a *Aut*.gr file
Automorphisms:
0:  1234
