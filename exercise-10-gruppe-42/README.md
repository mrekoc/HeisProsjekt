# Exercise10
The following webpages contain relevant information: http://www.doc.ic.ac.uk/~jnm/book/, http://www.doc.ic.ac.uk/~jnm/LTSdocumention/FSP-notation.html
## Introduction
1. Download the LTSAtool.zip from Blackboard. 
2. Extract the files to a folder of your choosing. 
3. Find LTSA.jar and open it with Java.

## Part 1 - Deadlock
The absence of deadlocks is a built-in safety criterion in LTSA.
1. Create a system with a deadlock. Does LTSA detect it?
2. From the state model we can easily check whether a deadlock exist by finding states with no exits. How can you detect a deadlock from the FSP model itself?

## Part 2 - Livelock
If nothing else is specified, LTSA uses the following progress criterion: From all states, all actions should be reachable within a finite number of steps.
1. Create a system with a livelock. This entails a subset of states without an exit. How does LTSA detect this?
2. Assume that the subset is not a livelock but normal behaviour. Create a progress property that contains only those states that are part of the livelock to get rid of the error (See http://www.doc.ic.ac.uk/~jnm/book/pdf/ch7.pdf for more on progress properties)

## Part 3 - Dining Philosophers
The dining philosophers problem is described in http://en.wikipedia.org/wiki/Dining_philosophers
1. Model a system with 3 philosophers and 3 forks. Demonstrate a deadlock.
2. Extend the FSM description to handle N philosophers by using indexing, prefixing, relabeling etc. How many philosophers can LTSA handle? Be careful, large numbers can cause unresponsiveness in your computer.
3. We want to remove the deadlock. Make one of the philosophers left handed (picks up forks in reverse order). Does that solve the problem? 
4. This also has consequences for fairness. Why? Can you come up with (or Google) a fair solution without deadlocks?
