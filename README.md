# Maggie (core)
Below readme is just a draft. To be finished.
## Components
1) Dashboard & Admin panel (Django + Django Admin)
2) Main data database (PostgreSQL)
3) Main task queues database (RabbitMQ or Redis - not decided yet)
4) Workers (Celery)
5) Scheduler (celery-beat)

```
+--CORE----------------------------+
|                                  |
|   +---+ <-a-  .^^^.  <------------A--- VARIOUS SOURCES
|   | 1 |  -b-> | 2 |  <------------A--- (adding data to database) 
|   +---+       'vvv'              |
|        \        ^   .-------------B---> VAR. SCS. (asking for updates)
|    ___  *c-.   f|  /             |
|   / | \     *>+---+      .^^^. <--C--- VARIOUS SOURCES
|  (  5--) -d-> | 4 | <-g- | 3 | <--C--- (adding tasks to queue) 
|   \___/       +---+      'vvv'   |
|     ^                      |     |
|     \_____e_______________.+     |
|                                  |
+----------------------------------+
```

## Data flows
### 1&2
(a) Reading the data from the main database (2) by the web dashboard (1)  
(b) Updating the data from dashboard and admin panel (1) to main database (2)  

### 1&3
(c) Reading tasks status from queues (3) in admin panel (1)  
(d) Adding tasks and tasks schedules from admin panel (1) to queues database (3)

### 2&e
(A) Receiving data to database (2) directly from external sources (e)

### 3&e
(C) Adding external tasks (e) to queue database (3)

### 3&4
(g) Workers (4) receiving data about queued tasks from queue database (3)

(d) Running scheduled tasks from scheduler (5) on workers (4)
(e)

(f)
(g)

(A)
(B)
(C)