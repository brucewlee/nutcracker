from typing import List, Set, Optional
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



    def _is_correct(self, instance: MCQInstance) -> bool:
        # First, try rule-based parsing
        found_options = self._parse_model_response_rule_based(instance.model_response)
        
        # If rule-based parsing fails or is ambiguous and intent matching is not disabled, use intent-matching
        if not found_options and not self.disable_intent_matching:
            model_response_set = self._parse_model_response_intent_matching(instance.model_response)
        elif not found_options:
            return False  # Consider not rule-matched responses as wrong if intent matching is disabled

        correct_options_set = set(instance.correct_options)
        return model_response_set == correct_options_set



    @staticmethod
    def _parse_model_response_rule_based(response: str) -> Optional[Set[str]]:
        """
        Parse the model response based on rule-based criteria.

        - Strips and uppercases the response.
        - Checks if the response matches a single alphabet.
        - Returns None if more than one option is found.

        Args:
            response (str): The response from the model.

        Returns:
            Optional[Set[str]]: A set containing the single valid option found in the response, or None if the criteria are not met.
        """
        # Strip, uppercase, and filter only alphabetical characters
        cleaned_response = set(filter(str.isalpha, response.strip().upper()))

        # Define valid options
        valid_options = {chr(i) for i in range(ord('A'), ord('Z') + 1)}

        # Intersect the cleaned response with valid options to filter out any invalid characters
        found_options = cleaned_response.intersection(valid_options)

        # Return None if more than a single option is found
        if len(found_options) != 1:
            return None

        return found_options



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

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": 'You respond with the letter option (like A, B, D, or None) separated by commas and nothing else.'},
                {"role": "user", "content": few_shot}
            ],
            seed=123456789,
            temperature=1
        )

        interpreted_response = completion.choices[0].message.content.strip().upper()
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