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
How long is this task?
"""
# prints -> 1172
print(len(my_task_A))

"""
A Task object is a collection of Instance objects
"""
# prints -> <nutcracker.data.instance.MCQInstance object at 0x10597e890>
print(my_task_A[0]) 

"""
An Instance object is full of useful information
"""
# prints -> dict_keys(['config', 'example_data_list', 'centerpiece', 'options', 'correct_options', 'user_prompt', 'model_response', 'answers', 'response_correct'])
print(vars(my_task_A[0].keys())) 

"""
Let's view AI2 Reasoning Challenge's first question and answer
"""
# prints-> Question: An astronomer observes that a planet rotates faster after a meteorite impact. Which is the most likely effect of this increase in rotation?. 
# Options: ['Planetary density will decrease.', 'Planetary years will become longer.', 'Planetary days will become shorter.', 'Planetary gravity will become stronger.']. 
# Answer: ['C']
print(f"Question: {my_task_A[0].centerpiece}. \nOptions: {my_task_A[0].options}. \nAnswer: {my_task_A[0].correct_options}") 

"""
But with few-shot evalutaion, this is what actually goes into a model
"""
# prints -> User Prompt: Question: Juan and LaKeisha roll a few objects down a ramp. They want to see which object rolls the farthest. What should they do so they can repeat their investigation? A. Put the objects in groups. B. Change the height of the ramp. C. Choose different objects to roll. D. Record the details of the investigation. Answer: D 
#Question: High-pressure systems stop air from rising into the colder regions of the atmosphere where water can condense. What will most likely result if a high-pressure system remains in an area for a long period of time? A. fog B. rain C. drought D. tornado Answer: C 
#<...skipped>
#Question: Amanda and Jake learned about kinetic and potential forms of energy within a simple electrical circuit. The circuit they are studying has a battery, wires, and a light bulb. Which is a form of potential energy in the circuit? A. chemical energy in the battery B. light energy from the light bulb C. heat energy lost from the electric wires D. electrical energy moving through the light bulb Answer: A 
#Question: An astronomer observes that a planet rotates faster after a meteorite impact. Which is the most likely effect of this increase in rotation? A. Planetary density will decrease. B. Planetary years will become longer. C. Planetary days will become shorter. D. Planetary gravity will become stronger. Answer: 
print(f"User Prompt: {my_task_A[0].user_prompt}.") 

"""
Two Tasks can be merged to create a Pile
"""
my_pile = Pile([my_task_A, my_task_B])

"""
A Pile is a collection of Instances within Tasks, not a collection of Tasks
"""
# <nutcracker.data.instance.MCQInstance object at 0x1045319c0>
print(my_pile[0]) 
```

### Conducting Experiments
```python
from nutcracker.data import Task, Pile
import os, logging
logging.basicConfig(level=logging.INFO)
os.environ["OPENAI_API_KEY"] = "Your OpenAI API Key"

my_task_A = Task.load_from_db(
    task_name = 'arc-challenge',
    db_directory = 'nutcracker-db/db'
    )

"""
Let's evaluate OpenAI's GPT-3.5. Nutcracker connects to LiteLLM so you can do it with ease.
"""
from nutcracker.model import Litellm
chatgpt = Litellm(model="gpt-3.5-turbo", max_tokens=100)

"""
Now let's define our experiment. Nutcracker organizes experiments in three levels: Schema, Inquiry, and Study. 
For now, let's try Schema, the smallest level of experiment that you can conduct.
A Schema object connects the model and Nutcracker's data.
Let's evaluate the first five instances from our Task A.
"""
import copy
demo_task = copy.deepcopy(my_task_A[:5])

from nutcracker.runs import Schema
new_experiment = Schema(model=chatgpt, data=demo_task)
new_experiment.run()

"""
Running the experiment updates each Instance object that was originally in the given Task.
Let's see what the model responded to the first question.
"""
# prints -> Question: An astronomer observes that a planet rotates faster after a meteorite impact. Which is the most likely effect of this increase in rotation? 
#Options: ['Planetary density will decrease.', 'Planetary years will become longer.', 'Planetary days will become shorter.', 'Planetary gravity will become stronger.'] 
#Model Response: C. Planetary days will become shorter.
#Answer: ['C']
print(f"Question: {demo_task[0].centerpiece} \nOptions: {demo_task[0].options} \nModel Response: {demo_task[0].model_response} \nAnswer: {demo_task[0].correct_options}") 

"""
GPT-3.5 got the first question correct! 
Evaluators in Nutcracker compares each Instance's model_response to correct_options to give score.
"""
from nutcracker.evaluator import MCQEvaluator
new_evaluation = MCQEvaluator(data=demo_task, evaluation_method="intent-matching")
new_evaluation_results = new_evaluation.run()

print(f"Accuracy: {new_evaluation_results*100}%")
```