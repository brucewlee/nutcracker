from typing import Set, Optional
#
from nutcracker.data.instance import MCQInstance
#
#
from openai import OpenAI
import openai
#
#
#
class MCQJudgeAlpha:
    def __init__(self):
        # Use the kwargs as needed for configuration
        # Example: self.some_setting = kwargs.get('some_setting', default_value)
        pass



    def is_correct(self, instance: MCQInstance) -> bool:
        found_options = self._parse_model_response_intent_matching(instance.model_response)
        correct_options_set = set(instance.correct_options)

        return found_options == correct_options_set



    @staticmethod
    def _parse_model_response_intent_matching(response: str) -> Set[str]:
        client = OpenAI()
        few_shot = f"""
        Your job is: given a response, determine to which option the response is potining to. That is, classify a given response to discrete labels: A, B, C, D, E, ..., Z, or None (if the response is pointing to multiple labels give multiple).

        Examples:

        Response: 'The answer is A.'
        Interpretation: A

        Response: 'I believe B and C are correct.'
        Interpretation: B, C

        Response: 'Definitely D.'
        Interpretation: D

        Response: 'Although many think it's A, the correct answer is actually D.'
        Interpretation: D

        Response: 'A seems right, but after further analysis, B and D are more accurate.'
        Interpretation: B, D

        Response: 'Question: Which of the following will cause a factory'
        Interpretation: None

        Response: 'Options A and B are incorrect, so it must be C.'
        Interpretation: C

        Response: 'Please choose the answer you think is correct and press the submit answer button.'
        Interpretation: None

        Response: 'Either A or B could work, but I lean towards B.'
        Interpretation: B

        Response: 'A. There are no rules that all artificial intelligences currently follow.'
        Interpretation: A

        Response: 'Question: The process of creating new concepts, ideas, and innovations is called A. invention. B. creativity. C. technology. D. entrepreneurship.? Answer: B'
        Interpretation: None
        
        Response: '{response}' 
        Interpretation: 
        """

        interpreted_response = None
        while interpreted_response is None:
            try:
                completion = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": 'You respond with the letter option (like A, B, D, or None) separated by commas and nothing else.'},
                        {"role": "user", "content": few_shot}
                    ],
                    seed=123456789,
                    timeout=15,
                    temperature=1
                )
                interpreted_response = completion.choices[0].message.content.strip().upper()
                break
            except openai.BadRequestError:
                interpreted_response = "None"
            except KeyboardInterrupt:
                sys.exit()

        return set(interpreted_response.split(', ')) if interpreted_response else set()