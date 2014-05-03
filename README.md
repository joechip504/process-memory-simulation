#Operating Systems Project 2
##Joe Pringle

#Usage
Written using python3. Sample usage:

```
python3 memsim.py [-q] <input-file> {noncontig | first | best | worst | next}

python3 memsim.py -q firstnext.txt first
python3 memsim.py firstnext.txt next
```

#Notes
* If the user is controlling the loop, output is **only** displayed at
the time the user specifies, and at time 0. Without -q specified, defragmentation will NOT be shown. 
I changed this after reading the clarifications on the project description. 

* If values are ever entered out of increasing order, the simulation
just skips to the end.

* All simulation functionality comes through the run_simulation function
in memsim.py. run_simulation takes a function as an argument and uses
that to place blocks in memory. All allocation algorithms are 
located in allocation_algorithms.py

