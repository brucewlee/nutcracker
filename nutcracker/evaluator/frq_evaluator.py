from typing import List, Set, Optional
import logging
#
from nutcracker.data.instance import FRQInstance
from nutcracker.utils import TqdmLoggingHandler
#
#
from openai import OpenAI
#
#
#
class FRQEvaluator:
    def __init__(self, data: List[FRQInstance]) -> None:
        self.data = data
        self._control_logging()



    def run(self, round_digits: int = 5) -> float:
        correct_count = 0
        if self.logger.getEffectiveLevel() <= logging.INFO:
            for instance in TqdmLoggingHandler(self.data, logger=self.logger, desc="Processing Instances"):
                is_correct = self._is_correct(instance)
                instance.response_correct = is_correct  # Update the instance attribute here
                if is_correct:
                    correct_count += 1
        else:
            for instance in self.data:
                is_correct = self._is_correct(instance)
                instance.response_correct = is_correct  # Update the instance attribute here
                if is_correct:
                    correct_count += 1

        accuracy = correct_count / len(self.data) if len(self.data) > 0 else 0.0
        return round(accuracy, round_digits) 



    def _is_correct(self, instance: FRQInstance) -> bool:
        found_options = self._parse_model_response_intent_matching(instance.model_response, instance.answer)

        instance.response_parsed = found_options
        if 'true' in found_options.lower() and 'false' not in found_options.lower():
            return True
        elif 'true' not in found_options.lower() and 'false' in found_options.lower():
            return False
        else:
            return False



    @staticmethod
    def _parse_model_response_intent_matching(response: str, answer: str) -> Set[str]:
        client = OpenAI()
        few_shot = f"""
        Your job is: given a response, determine if the answer is correct or not. Say True or False and nothing else.

        Examples:
        
        Answer: '\\frac{625}{648}'
        Response: 'It's 625/648.'
        Interpretation: True

        Answer: '\\frac{2}{5}'
        Response: 'It's 4/6'
        Interpretation: False
        
        Answer: '{answer}'
        Response: '{response}'
        Interpretation: 
        """

        interpreted_response = None
        while interpreted_response is None:
            try:
                completion = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": 'You respond with True or False and nothing else.'},
                        {"role": "user", "content": few_shot}
                    ],
                    seed=123456789,
                    timeout=15,
                    temperature=1
                )
                interpreted_response = completion.choices[0].message.content.strip()
                break
            except KeyboardInterrupt:
                sys.exit()
        print(interpreted_response)
        return interpreted_response

    

    def _control_logging(
            self,
        ) -> None:
        """Control logging for Schema

        Args:
            None
        
        Raises:
            None
        
        Returns:
            None
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"runnable FRQEvaluator -> created with {len(self.data.instances)} instances.")