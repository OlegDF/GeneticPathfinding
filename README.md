# GeneticPathfinding
A robot tries to navigate through obstacles using randomness and crossbreeding

A point starts out in (0, 0) and its position is changed every TIME_DELTA seconds.
Every time after it moves, a force is applied that may be a vector of any direction, but with a length no more than MAX_FORCE.
This acceleration changes the point's current speed that determines how it will move in the next step; the initial speed is zero (the point starts out motionless).
Thus, a sequence of forces defines the point's path, but the number of steps is restricted to MAX_LENGTH.
The point must end up at the final point of (1, 1) and stop there (have a speed of 0).
It is also restricted to the square between (0, 0) and (1, 1).

The algorithm first generates a number of random sequences of forces, then grants them a score according to how close they come to arriving at the target and stopping, as well as how little time they spend outside the square bounds or inside the obstacles.
From this first generation, the next one is created. The 10% best performing attempts to reach the end are carried over with only mutation (small random changes to every force) and the rest are put into the parent pool.
From among the parents, two force sequences may be chosen with probabilities according to their performance, and these are crossbred (each pair of forces with the same number produces an average). 
The result is put into the new generation of attempts, until it reaches the same population as the initial one.
The process repeats for a set number of generations, at which point the result (the best-performing 10% of the final generation) is presented pon a chart.
