import os
#
from nutcracker.evaluator.mcq_evaluator import MCQEvaluator
from nutcracker.data.instance import MCQInstance
#
#
import pytest
#
#
#
@pytest.mark.parametrize("model_response, correct_options, expected", [
    # Test case 1: Direct single choice
    ("A", ["A"], True),
    # Test case 2: Direct multiple choices
    ("B, C", ["B", "C"], True),
    # Test case 3: Sentence with single choice
    ("I think the answer is B", ["B"], True),
    # Test case 4: Sentence with multiple choices
    ("The correct options are A and D", ["A", "D"], True),
    # Test case 5: Irrelevant response
    ("I'm not sure about the answer", ["A"], False),
    # Test case 6: No response
    ("", ["A"], False),
    # Test case 7: Partially correct multiple choices
    ("B, C", ["B", "C", "D"], False),
    # Test case 8: Incorrect format
    ("Option A is correct", ["A"], True),
    # Test case 9: Answer embedded in a complex sentence
    ("After careful consideration, I believe the correct answer is B", ["B"], True),
    # Test case 10: Multiple answers in a complex sentence
    ("Based on the data, the answers could be A, B, and C", ["A", "B", "C"], True),
    # Test case 11: Incorrect answer in sentence
    ("It seems like B is correct, but actually, the correct answer is A", ["A"], True),
    # Test case 12: Answer with distractors in the sentence
    ("Although B and C are close, the most accurate answer is A", ["A"], True),
    # Test case 13: Ambiguous answer
    ("It's either A or B, hard to tell", ["A"], False),
    # Test case 14: Answer within a question
    ("Is the answer A? No, it's actually B", ["B"], True),
    # Test case 15: Answer with negation
    ("The answer is definitely not A", ["A"], False),
    # Test case 16: Answer with affirmation
    ("Yes, the answer is A", ["A"], True),
    # Test case 17: Multiple correct and incorrect options
    ("A, B, C are possible, but only A and C are correct", ["A", "C"], True),
    # Test case 18: Answer in a misleading format
    ("Some might say B, but no, the answer is A", ["A"], True),
    # Test case 19: Answer with additional commentary
    ("The answer is A, though it was a tricky question", ["A"], True),
    # Test case 20: Answer in a quotation
    ("As the saying goes, 'A is the key to success'", ["A"], True),
    # Test case 21: Answer with Redundant Information
    ("The answer is definitely B, without a doubt B", ["B"], True),
    # Test case 22: Answer in a List Format
    ("The answers are: 1) A, 2) C", ["A", "C"], True),
    # Test case 23: Answer with Conflicting Information
    ("Most people think it's B, but I am sure it's A", ["A"], True),
    # Test case 24: Answer with a Question and Response
    ("Is it B? No, after checking, it's A", ["A"], True),
    # Test case 25: Answer with Multiple Sentences and Distraction
    ("Considering all factors, B is the best choice.", ["B"], True),
    # Test case 26: Answer with Conditional Statements
    ("It's definitely C", ["C"], True),
    # Test case 27: Answer with a Misleading Preface
    ("At first glance, one might say B. Upon closer examination, it's clearly A.", ["A"], True),
    # Test case 28: Answer in a Conversational Style
    ("Well, you know, I was thinking B, but no, it's A for sure.", ["A"], True),
    # Test case 29: Answer with Hypotheticals
    ("is A.", ["A"], True),
    # Test case 30: Answer with an Indirect Confirmation
    ("After analyzing, it can be concluded that A is the most plausible.", ["A"], True),

    # Additional test cases including letters like F, G, E
    ("The answer is definitely E", ["E"], True),
    ("I'm torn between F and G, but it's probably F", ["F"], True),
    ("It could be E or F, but I'm leaning towards G", ["G"], True),
    ("Options E and G are possible, but the correct one is F", ["F"], True),
    ("G seems correct, but on second thought, it's E", ["E"], True)
])
def test_mcq_evaluator(model_response, correct_options, expected):
    os.environ["OPENAI_API_KEY"] = "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"
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
    evaluator = MCQEvaluator([instance], evaluation_method="intent-matching")

    # Check if the instance is evaluated correctly
    assert evaluator._is_correct(instance) == expected
