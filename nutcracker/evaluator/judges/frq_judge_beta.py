from typing import Optional, List, Set
#
from nutcracker.data.instance import FRQInstance
#
#
class FRQJudgeBeta:
    def __init__(self):
        pass



    def is_correct(self, instance: FRQInstance) -> bool:
        found_options = self._parse_model_response_rule_based(instance.model_response)
        correct_options_set = set(instance.correct_options)
        return found_options == correct_options_set

    

    @staticmethod
    def _parse_model_response_rule_based(response: str) -> Optional[Set[str]]:
        """
        Parse the model response based on rule-based criteria.

        - Strips and uppercases the response.
        """
        # Strip, uppercase
        cleaned_response = response.strip().upper()

        return cleaned_response