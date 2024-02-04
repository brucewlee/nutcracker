# Nutcracker: *Lightening Fast LLM Evaluation*

## Installation

**Install Nutcracker**
```bash
git clone https://github.com/Walnut-Research/nutcracker
pip install -e nutcracker
```

**Download Nutcracker DB**
```bash
git clone https://github.com/Walnut-Research/nutcracker-db
```

## Understanding Nutcracker
### Instance, Task, Pile
```python
from nutcracker.data import Task, Pile
import logging
logging.basicConfig(level=logging.INFO)

"""
Let's play with the AI2 Reasoning Challenge and 
MMLU College Computer Science
"""

my_task_A = Task.load_from_db(
    task_name = 'arc-challenge',
    db_directory = 'nutcracker-db/db'
    )

my_task_B = Task.load_from_db(
    task_name = 'mmlu-college-computer-science',
    db_directory = 'nutcracker-db/db'
    )

"""
This is Nutcracker's Task object
"""
# prints -> <nutcracker.data.task.Task object at 0x104654100>
print(my_task_A) 

"""
And a Task object is a collection of Instance objects
"""
# prints -> <nutcracker.data.instance.MCQInstance object at 0x10597e890>
print(my_task_A[0]) 

"""
Two Tasks can be merged to create a Pile
"""
my_pile = Pile([my_task_A, my_task_B])

"""
A Pile is a collection of Instance objects from both Tasks
"""
print(my_pile[0]) 

# How long is this task?
# prints -> 1172
print(len(my_task_A))
```