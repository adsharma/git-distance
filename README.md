git-distance
============

Social graph analysis for public git repos

The code could be used to analyze git logs for tracking how code ends
up in a maintainer's repo.

Also included is sample output from linux.git. Interpretation:

937 1.46958377801 Tejun Heo {1: 541, 2: 360, 3: 31, 4: 2, 5: 3}

Tejun had 937 commits, 541 of them were directly applied by Linus.
360 were committed to another maintainer's repo and then merged etc.

TODO:
====

* Increment the path length only on seeing a merge commit.
* Visualization
