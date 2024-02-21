from openai import OpenAI
import os, logging, sys
logging.basicConfig(level=logging.INFO)
logging.getLogger('httpx').setLevel(logging.CRITICAL)
os.environ["OPENAI_API_KEY"] = "XXX"
client = OpenAI()

class ChatGPT:
    def __init__(self):
        self.model = "gpt-3.5-turbo"

    def respond(self, user_prompt):
        response_data = None
        while response_data is None:
            try:
                completion = client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": f"{user_prompt}"}
                    ],
                    timeout=15,
                )
                response_data = completion.choices[0].message.content
                break
            except KeyboardInterrupt:
                sys.exit()
            except:
                print("Request timed out, retrying...")
        return response_data






from nutcracker.data import Task, Pile
from nutcracker.runs import Schema
from nutcracker.evaluator import MCQEvaluator, generate_report

# this db_directory value should work off-the-shelf if you cloned both repositories in the same directory
truthfulqa = Task.load_from_db(task_name='truthfulqa-mc1', db_directory='nutcracker-db/db')

# sample 20 for demo
truthfulqa.sample(20, in_place=True)

# running this experiment updates each instance's model_response property in truthfulqa data object with ChatGPT responses
experiment = Schema(model=ChatGPT(), data=truthfulqa)
experiment.run()

# running this evaluation updates each instance's response_correct property in truthfulqa data object with evaluations
evaluation = MCQEvaluator(data=truthfulqa)
evaluation.run()

for i in range (0, len(truthfulqa)):
    print(truthfulqa[i].user_prompt)
    print(truthfulqa[i].model_response)
    print(truthfulqa[i].correct_options)
    print(truthfulqa[i].response_correct)
    print()

print(generate_report(truthfulqa, save_path='accuracy_report.txt'))