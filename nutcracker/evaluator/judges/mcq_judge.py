from typing import Set, Optional
#
from nutcracker.data.instance import MCQInstance
from nutcracker.models import *
#
#
class MCQJudge:
    def __init__(self, model):
        self.model = model


    def is_correct(self, instance: MCQInstance) -> bool:
        # First, try rule-based parsing
        found_options = self._parse_model_response_rule_based(instance.model_response)

        if instance.correct_options:
            correct_options_set = set(instance.correct_options)
        else:
            correct_options_set = None
        
        # If rule-based parsing fails or is ambiguous and intent matching is not disabled, use intent-matching
        if not found_options:
            found_options = self._parse_model_response_intent_matching(instance.model_response)
        elif not found_options:
            return False  # Consider not rule-matched responses as wrong if intent matching is disabled

        instance.response_parsed = found_options

        return found_options == correct_options_set, found_options



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



    def _parse_model_response_intent_matching(self, response: str) -> Set[str]:
        few_shot = f"""
        Your job is: given a response, determine to which option the response is potining to. That is, classify a given response to discrete labels: A, B, C, D, E, ..., Z, or None (if the response is pointing to multiple labels give multiple).

        Example 1 - Clear Single Response
        Response: 'The answer is A.'
        Interpretation: A

        Example 2 - Clear Multi Response
        Response: 'I believe B and C are correct.'
        Interpretation: B, C

        Example 3 - Clear Single Response
        Response: 'Definitely D.'
        Interpretation: D

        Example 4 - Clear Single Response
        Response: 'Although many think it's A, the correct answer is actually D.'
        Interpretation: D

        Example 5 - Clear Multi Response
        Response: 'A seems right, but after further analysis, B and D are more accurate.'
        Interpretation: B, D

        Example 6 - Not a Response
        Response: 'Question: Which of the following will cause a factory'
        Interpretation: None

        Example 7 - Clear Single Response
        Response: 'Options A and B are incorrect, so it must be C.'
        Interpretation: C

        Example 8 - Not a Response
        Response: 'Please choose the answer you think is correct and press the submit answer button.'
        Interpretation: None

        Example 9 - Clear Single Response
        Response: 'Either A or B could work, but I lean towards B.'
        Interpretation: B
        
        Example 10 - Clear Single Response
        Response: 'A. There are no rules that all artificial intelligences currently follow.'
        Interpretation: A

        Example 11 - Response Includes Another Question
        Response: 'Question: The process of creating new concepts, ideas, and innovations is called A. invention. B. creativity. C. technology. D. entrepreneurship.? Answer: B'
        Interpretation: None
        
        Example 12 - Clear Single Response
        Response: 'Answer: E. Like you.'
        Interpretation: E

        Now consider,
        Response: '{response}' 
        Interpretation: 
        """

        interpreted_response = None
        while interpreted_response is None:
            try:
                completion = self.model.respond(
                    'You respond with the letter option (like A, B, D, F, or None) separated by commas and nothing else.\n\n' + few_shot
                )
                interpreted_response = completion.strip().upper()
                break
            except KeyboardInterrupt:
                sys.exit()

        return set(interpreted_response.split(', ')) if interpreted_response else set()