from typing import Optional, List, Set
#
from nutcracker.data.instance import MCQInstance
#
#
class MCQEngineBeta:
    def __init__(self):
        pass



    def is_correct(self, instance: MCQInstance) -> bool:
        found_options = self._parse_model_response_rule_based(instance.model_response)
        correct_options_set = set(instance.correct_options)
        return found_options == correct_options_set

    

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