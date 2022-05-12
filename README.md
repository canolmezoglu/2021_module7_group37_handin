# 2021_module7_group37<br>

### Implementation project for Graph Isomorphisms.<br>
In this directory we have all the files concerning the implementation of our Graph Isomorphism and Automorphism detection as specified in the Discrete Structures and Efficient Algorithms module of 2021 given by the University of Twente. This file contains the following subjects:

* contents of the directory
* manual
* paricipants

**file list:**<br>
```
2021_module7_group37
│   auto.py
│   basic_permutation_group.py
│   branching.py
│   disconnected.py
│   equivalence.py
│   graph.py
│   graph_io.py
│   main.py
│   old_branching.py
│   old_refinement.py
│   our_lib.py
│   permv2.py
│   preprocess.py
│   README.md
│   refinement.py
│   refinement_classes.py
│   tree.py
│   twins.py
│
├───graphs
│   │   bigtrees1.grl
│   │   bigtrees2.grl
│   │   bigtrees3.grl
│   │   cographs1.grl
│   │   colorref_largeexample_4_1026.grl
│   │   colorref_largeexample_6_960.grl
│   │   colorref_smallexample_2_49.grl
│   │   colorref_smallexample_4_16.grl
│   │   colorref_smallexample_4_7.grl
│   │   colorref_smallexample_6_15.grl
│   │   cref9vert_4_9.grl
│   │   cubes3.grl
│   │   cubes4.grl
│   │   cubes5.grl
│   │   cubes6.grl
│   │   cubes7.grl
│   │   cubes8.grl
│   │   cubes9.grl
│   │   modulesC.grl
│   │   modulesD.grl
│   │   products216.grl
│   │   products72.grl
│   │   threepaths10.gr
│   │   threepaths10240.gr
│   │   threepaths1280.gr
│   │   threepaths160.gr
│   │   threepaths20.gr
│   │   threepaths2560.gr
│   │   threepaths320.gr
│   │   threepaths40.gr
│   │   threepaths5.gr
│   │   threepaths5120.gr
│   │   threepaths640.gr
│   │   threepaths80.gr
│   │   torus144.grl
│   │   torus24.grl
│   │   torus72.grl
│   │   trees11.grl
│   │   trees36.grl
│   │   trees90.grl
│   │   wheeljoin14.grl
│   │   wheeljoin19.grl
│   │   wheeljoin25.grl
│   │   wheeljoin33.grl
│   │   wheelstar12.grl
│   │   wheelstar15.grl
│   │   wheelstar16.grl
│   │   __init__.py
│   │
│   ├───basic
│   │       basicAut1.gr
│   │       basicAut2.gr
│   │       basicGI1.grl
│   │       basicGI2.grl
│   │       basicGI3.grl
│   │       basicGIAut1.grl
│   │
│   ├───bonus
│   │       bonusAut1.gr
│   │       bonusAut2.gr
│   │       bonusAut3.grl
│   │       bonusAut4.grl
│   │       bonusAut5.grl
│   │       bonusGI1.grl
│   │       bonusGI2.grl
│   │       bonusGI3.grl
│   │       bonusGI4.grl
│   │       bonusGI5.grl
│   │
│   └───extra
│           competeAUT1.gr
│           competeGIAUT2.grl
│           competeGIAUT3.grl
│           competeGIAUT4.grl
│           competeGIAUT5.grl
│           competeGIAUT6.grl

```
<br><br>
**manual:**<br>
There are 2 ways of configuring our programme:<br>

*quickrun*: To use quickrun you need to pre-configure the quickrun variables at the bottom of our ```main.py``` before running it. The variables in question are: 
* ```qr_graph_set```: list of location strings of the graphs you want to run  (this has to be a list so the names need to be in between sqaure brackets and comma seperated, for an example look at any of the pre configured sets at the top of ```main.py```) 
* ```qr_count_aut```: boolean that indicates whether you want to also calculate Automorphisms next to Isomorphisms 
* ```qr_timed_run```: boolean that indicates wheher you want to have a calculation time printed as well as your results


*live configuration:* To enter live configuration you need to run ```main.py``` and answer the questions according to the instructions that appear on the terminal.

<br><br>
**participants:**<br>
Justin de Groot | s2293528<br>
Zoë van Herreveld | s2169312<br>
Reinier van der Horst | s2009552<br>
Can Olmezoglu | s2269236