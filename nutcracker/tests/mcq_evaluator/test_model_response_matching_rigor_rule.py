from nutcracker.evaluator.mcq_evaluator import MCQEvaluator
from nutcracker.data.instance import MCQInstance
#
#
import pytest
#
#
#
@pytest.mark.parametrize("model_response, correct_options, expected", [
    ("A", ["A"], True),
    ("B", ["B"], True),
    ("D", ["D"], True),
    ("The answer is D", ["D"], False),
    (" ", ["D"], False),
    ("I think the answer is most definitely...", ["D"], False),
])
def test_mcq_evaluator(model_response, correct_options, expected):
    # Mock config and test_data for MCQInstance
    mock_config = {
        "construction": "mcq",
        "user_prompt_template": {
            "centerpiece": "Example centerpiece: {centerpiece}",
            "options": "Options: {options}",
            "correct_options": "Correct options: {correct_options}"
        }
    }
    mock_test_data = {
        "centerpiece": "Example question",
        "options": ["A", "B", "C", "D"],
        "correct_options": correct_options
    }

    # Create MCQInstance
    instance = MCQInstance(mock_config, mock_test_data)
    instance.model_response = model_response

    # Initialize MCQEvaluator with the instance
    evaluator = MCQEvaluator([instance], evaluation_method="rule-matching")

    # Check if the instance is evaluated correctly
    assert evaluator._is_correct(instance) == expected
