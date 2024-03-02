from typing import Optional, List
#
from nutcracker.data.instance import MCQInstance
#
#
class MCQEngineGamma:
    def __init__(self):
        pass

    def is_correct(self, instance: MCQInstance) -> bool:
        # Extract the log probabilities for the first position token
        logprobs = instance.model_response_logprobs[0]

        # Extract the valid options (A, B, C, D, E) based on the length of the options list
        valid_options = [chr(ord('A') + i) for i in range(len(instance.options))]

        # Filter logprobs for valid options and ignore missing logprob values
        try:
            filtered_logprobs = [entry for entry in logprobs if entry[0] in valid_options and len(entry) > 1]
        except TypeError:
            # if only first position token was given
            logprobs = instance.model_response_logprobs
            filtered_logprobs = [entry for entry in logprobs if entry[0] in valid_options and len(entry) > 1]

        # If no valid logprobs are found, consider the response incorrect
        if not filtered_logprobs:
            return False

        # Find the option with the highest log probability
        best_option = max(filtered_logprobs, key=lambda x: x[1])[0].strip().upper()

        # Check if the best option matches any of the correct options
        return best_option in instance.correct_options