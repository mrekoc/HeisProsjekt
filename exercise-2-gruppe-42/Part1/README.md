# Mutex and Channel basics

### What is an atomic operation?
>   Processes run independently of each other. Avoid mutual exclusion
>   When a thread performs an atomic operation, the other threads see it as happening instantaneously.
>   Relative quick compared to locks
>   Disadvantage: limited set of operations

### What is a semaphore?
>   Datastructur used for solving synchronization problems
>   A thread is an integer that is incremented and decremented by threads. If the result after decrementation is negative the thread blocks itself until another thread increments the semaphore. 

>   ex: semaphore = -2, two threads (a,b) waiting. A thread (c) finished, increment sempahore = -1, thread (a) starts. ex: sempaphore = 3, three threads running.

### What is a mutex?
>   Mutual exclusion
>   Concurrency control
>   Avoids race conditions
>   A type of lock 

>   A semaphore can be a mutex, but a mutes can never be a semaphore

### What is the difference between a mutex and a binary semaphore?
>   Mutex: a lock
	someone tries to access while locked error occures
>   Binary semaphore: synchronizes 
	can constantly try and access something, until it is suddenly 	        	 avalible

### What is a critical section?
>   Shared variables
>   Needs ex. atomic operations, mutexes, semaphores 


### What is the difference between race conditions and data races?
 >  Data race: when 2 instructions from different threads access the same memory location, at least one of these accesses is a write and there is no synchronization that is mandating any particular order among these accesses.
 >  Race condition: is a flaw that occurs in the timing or the ordering of events that leads to erroneous program behavior. 

>   Many race conditions can be caused by data races, but this is not necessary.

### List some advantages of using message passing over lock-based synchronization primitives.
>   The biggest advantage of message passing is that it is easier to build massively parallel hardware. Message passing programming models tend to be more tolerant of higher communication latencies.
>   Easier to avoid concurrency bugs
>   Deadlock less likely

### List some advantages of using lock-based synchronization primitives over message passing.
>   Things are securely locked, the critical section is safe (?)
>   Simplier with less complicated structure (?)



