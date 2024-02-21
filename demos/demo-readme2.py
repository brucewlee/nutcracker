import requests

class LLaMA:
    def __init__(self):
        self.API_URL = "https://XXXX.endpoints.huggingface.cloud"

    def query(self, payload):
        headers = {
            "Accept" : "application/json",
            "Content-Type": "application/json" 
        }
        flag = False
        while flag == False:
            response = requests.post(self.API_URL, headers=headers, json=payload)
            if response.status_code == 200:
                flag = True
                
        return response.json()

    def respond(self, user_prompt):
        output = self.query({
            "inputs": f"<s>[INST] <<SYS>> You are a helpful assistant. You keep your answers short. <</SYS>> {user_prompt}",
        })
        return output[0]['generated_text']





from nutcracker.data import Pile
import logging,os
logging.basicConfig(level=logging.INFO)
os.environ["OPENAI_API_KEY"] = "XXXXX"
mmlu = Pile.load_from_db('mmlu','nutcracker-db/db')
print(mmlu.get_max_token_length_user_prompt())





from nutcracker.runs import Schema
mmlu.sample(n=2000, in_place = True)

experiment = Schema(model=LLaMA(), data=mmlu)
experiment.run()
mmlu.save_to_file('mmlu-llama.pkl')





loaded_mmlu = Pile.load_from_file('mmlu-llama.pkl')

from nutcracker.evaluator import MCQEvaluator, generate_report
evaluation = MCQEvaluator(data=loaded_mmlu, disable_intent_matching=False)
evaluation.run()

for i in range (0,len(loaded_mmlu)):
    print("\n\n\n---\n")
    print("Question:")
    print(loaded_mmlu[i].centerpiece)
    print(loaded_mmlu[i].options)
    print("\nOriginal Response:")
    print(loaded_mmlu[i].model_response)
    print("\nResponse Parsed:")
    print(loaded_mmlu[i].response_parsed)
    print("\nCorrect:")
    print(loaded_mmlu[i].correct_options)
    print("\nCorrect:")
    print(loaded_mmlu[i].correct_options)


print(generate_report(loaded_mmlu, save_path='accuracy_report.txt'))