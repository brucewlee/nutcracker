from typing import List, Set
#
from nutcracker.data.instance import MCQInstance
#
#
from openai import OpenAI
#
#
#
class MCQEvaluator:
    def __init__(self, data: List[MCQInstance], evaluation_method: str = "rule-matching") -> None:
        self.data = data
        self.evaluation_method = evaluation_method



    def run(self) -> float:
        correct_count = 0
        for instance in self.data:
            if self._is_correct(instance):
                correct_count += 1

        return round(correct_count / len(self.data),5) if self.data else 0.0



    def _is_correct(self, instance: MCQInstance) -> bool:
        if self.evaluation_method == "rule-matching":
            model_response_set = self._parse_model_response_rule_based(instance.model_response)
        elif self.evaluation_method == "intent-matching":
            model_response_set = self._parse_model_response_intent_matching(instance.model_response)
        else:
            raise ValueError(f"Unknown evaluation method: {self.evaluation_method}")

        correct_options_set = set(instance.correct_options)
        return model_response_set == correct_options_set



    @staticmethod
    def _parse_model_response_rule_based(response: str) -> Set[str]:
        if not response:
            return set()
        
        options = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        found_options = set()
        response_set = set(response.upper())

        for option in response_set:
            if option in options:
                found_options.add(option)

        # Only consider response valid if no other options are found
        if found_options - set(response.upper()):
            return set()
        
        return found_options



    @staticmethod
    def _parse_model_response_intent_matching(response: str) -> Set[str]:
        client = OpenAI()
        few_shot = f"""
        Example 1:
        Response: 'The answer is A.'
        Interpretation: A

        Example 2:
        Response: 'I believe B and C are correct.'
        Interpretation: B, C

        Example 3:
        Response: 'Definitely D.'
        Interpretation: D

        Example 4:
        Response: 'Options A and B are incorrect, so it must be C.'
        Interpretation: C

        Example 5:
        Response: 'Although many think it's A, the correct answer is actually D.'
        Interpretation: D

        Example 6:
        Response: 'A seems right, but after further analysis, B is more accurate.'
        Interpretation: B

        Example 7:
        Response: 'Either A or B could work, but I lean towards B.'
        Interpretation: B

        Example 8:
        Response: 'Options include A, B, C; however, C is the most plausible.'
        Interpretation: C
        
        Question:
        Example: '{response}' 
        Interpretation: 
        """

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": 'You respond with the letter option (like A, B, D, or None) separated by commas and nothing else.'},
                {"role": "user", "content": few_shot}
            ],
            seed=123456789,
            temperature=1
        )

        interpreted_response = completion.choices[0].message.content.strip()
        return set(interpreted_response.split(', ')) if interpreted_response else set()