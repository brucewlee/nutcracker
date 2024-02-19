# Nutcracker

<p align="center">
<img src="resources/w_500.png" width="200"/>
</p>

LLM Evaluation, like LM-Eval-Harness but more straightforward data management

---

## Installation

**Install Nutcracker**
```bash
git clone https://github.com/brucewlee/nutcracker
pip install -e nutcracker
```

**Download Nutcracker DB**
```bash
git clone https://github.com/brucewlee/nutcracker-db
```

## QuickStart
### Case Study: Evaluate (Any) LLM API on TruthfulQA
##### STEP 1: Define Model
- Define a simple model class with a "*respond(self, user_prompt)*" function. 
- We will use OpenAI here. But really, any api can be evaluated if the "*respond(self, user_prompt)*" function that returns LLM response in string exists. Get creative (Hugginface API, Anthropic API, Replicate API, OLLaMA, and etc.)
```python
from openai import OpenAI
os.environ["OPENAI_API_KEY"] = ""
client = OpenAI()

class ChatGPT:
    def __init__(self):
        self.model = "gpt-3.5-turbo-0125"

    def respond(self, user_prompt):
        completion = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": f"{user_prompt}"}
            ]
        )
        response_data = completion.choices[0].message.content

        return response_data
```
##### STEP 2: Run Evaluation
```python
from nutcracker.data import Task, Pile
from nutcracker.runs import Schema
from nutcracker.evaluator import MCQEvaluator

# this db_directory value should work off-the-shelf if you cloned both repositories in the same directory
truthfulqa = Task.load_from_db(task_name='truthfulqa-mc1', db_directory='/nutcracker-db/db')

experiment = Schema(model=ChatGPT(), data=truthfulqa)
# running this experiment updates truthfulqa data object with ChatGPT responses
experiment.run()

evaluation = MCQEvaluator(data=truthfulqa, evaluation_method="intent-matching")
evaluation.run()
```

### Case Study: Task vs. Pile? Evaluating LLaMA on MMLU
##### STEP 1: Understand the basis of Nutcracker
- Despite our lengthy history of model evaluation, my understanding of the field is that we have not reached a clear consensus on what a "benchmark" is (*Is MMLU a "benchmark"? Is Huggingface Open LLM leaderboard a "benchmark"?*). 
- Instead of using the word benchmark, Nutcracker divides the data structure into Instance, Task, and Pile (See blog post: [HERE](https://brucewlee.medium.com/nutcracker-instance-task-pile-38f646c1b36d))
- Nutcracker DB is constructed on the Task-level but you can call multiple Tasks together on the Pile-level.
<p align="center">
<img src="resources/w_2100.png" width="400"/>
</p>

##### STEP 2: Define Model
- Since we've tried OpenAI API above, let's now try Hugginface Inference Endpoint. Most open-source models are accessible through this option. (See blog post: [HERE](https://brucewlee.medium.com/nutcracker-evaluating-on-huggingface-inference-endpoints-6e977e326c5b))

## Tutorials
- Evaluating on HuggingFace Inference Endpoints -> [HERE / Medium](https://brucewlee.medium.com/nutcracker-evaluating-on-huggingface-inference-endpoints-6e977e326c5b)
- Understanding Instance-Task-Pile -> [HERE / Medium](https://brucewlee.medium.com/nutcracker-instance-task-pile-38f646c1b36d)
