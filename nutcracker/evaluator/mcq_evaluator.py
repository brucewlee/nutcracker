from typing import List, Set
import logging
#
from nutcracker.data.instance import MCQInstance
from nutcracker.utils import TqdmLoggingHandler
#
#
from openai import OpenAI
#
#
#
class MCQEvaluator:
    def __init__(self, data: List[MCQInstance], disable_intent_matching: bool = False) -> None:
        self.data = data
        self.disable_intent_matching = disable_intent_matching
        self._control_logging()



    def run(self, round_digits: int = 5) -> float:
        correct_count = 0
        for instance in TqdmLoggingHandler(self.data, logger=self.logger, desc="Processing Instances"):
            is_correct = self._is_correct(instance)
            instance.response_correct = is_correct  # Update the instance attribute here
            if is_correct:
                correct_count += 1

        accuracy = correct_count / len(self.data) if len(self.data) > 0 else 0.0
        return round(accuracy, round_digits) 



    def _is_correct(self, instance: MCQInstance) -> bool:
        # First, try rule-based parsing
        model_response_set = self._parse_model_response_rule_based(instance.model_response)
        
        # If rule-based parsing fails or is ambiguous and intent matching is not disabled, use intent-matching
        if not model_response_set and not self.disable_intent_matching:
            model_response_set = self._parse_model_response_intent_matching(instance.model_response)
        elif not model_response_set:
            return False  # Consider not rule-matched responses as wrong if intent matching is disabled

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

        Response: 'Question: The process of creating new concepts, ideas, and innovations is called A. invention. B. creativity. C. technology. D. entrepreneurship.? Answer: B'
        Interpretation: None
        
        Response: '{response}' 
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
        self.logger.info(f"runnable MCQEvaluator -> created with {len(self.data.instances)} instances.")