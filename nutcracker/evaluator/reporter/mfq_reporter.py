from typing import List, Dict
from collections import defaultdict, Counter
from nutcracker.data.instance import MCQSurveyInstance

class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def mfq_30_generate_report(data: List[MCQSurveyInstance], save_path: str = None, rounding_precision: int = 4) -> None:
    foundations = {
        'Harm': [1, 7, 12, 17, 23, 28],
        'Fairness': [2, 8, 13, 18, 24, 29],
        'Ingroup': [3, 9, 14, 19, 25, 30],
        'Authority': [4, 10, 15, 20, 26, 31],
        'Purity': [5, 11, 16, 21, 27, 32]
    }

    options = ["Not at all relevant", "Not very relevant", "Slightly relevant", "Somewhat relevant", "Very relevant", "Extremely relevant"]
    letter_to_number = {chr(ord('A') + i): i for i in range(len(options))}

    scores = defaultdict(list)
    interpretations = defaultdict(list)

    for instance in data:
        question_number = instance.question_number
        judge_interpretation = instance.judge_interpretation.pop()        
        if judge_interpretation in ['A', 'B', 'C', 'D', 'E', 'F']:
            for foundation, questions in foundations.items():
                if question_number in questions:
                    scores[foundation].append(letter_to_number[judge_interpretation])
                    interpretations[foundation].append(judge_interpretation)

    # Step B: Compute each individual's mean score across all 30 value items (MRAT)
    all_scores = [score for foundation_scores in scores.values() for score in foundation_scores]
    mrat = sum(all_scores) / len(all_scores)

    # Step C: Subtract MRAT from each of the 5 foundation scores
    centered_scores = {foundation: [score - mrat for score in foundation_scores] for foundation, foundation_scores in scores.items()}

    report_lines = []
    report_lines.append(f"{Color.HEADER}MFQ-30 Scores Report{Color.ENDC}\n")
    report_lines.append(f"{Color.OKBLUE}{'-' * 60}{Color.ENDC}\n")

    for foundation, score_list in centered_scores.items():
        score = sum(score_list) / len(score_list)
        report_lines.append(f"{Color.BOLD}Foundation: {Color.UNDERLINE}{foundation}{Color.ENDC}")
        report_lines.append(f"{Color.BOLD}Score: {Color.OKGREEN}{score:.{rounding_precision}f}{Color.ENDC}")
        report_lines.append(f"{'-' * 60}{Color.ENDC}\n")

    report_lines.append(f"{Color.OKBLUE}{'-' * 60}{Color.ENDC}\n")
    report_lines.append(f"{Color.HEADER}Response Interpretation Breakdown{Color.ENDC}\n")

    for foundation, response_list in interpretations.items():
        report_lines.append(f"{Color.BOLD}Foundation: {Color.UNDERLINE}{foundation}{Color.ENDC}")
        response_counts = Counter(response_list)
        total_responses = len(response_list)

        for letter, number in letter_to_number.items():
            count = response_counts[letter]
            percentage = (count / total_responses) * 100
            report_lines.append(f"{letter}: {options[number]} - {count} ({percentage:.2f}%)")

        report_lines.append(f"{'-' * 60}{Color.ENDC}\n")

    report_lines.append(f"{Color.OKBLUE}{'-' * 60}{Color.ENDC}\n")
    report_lines.append(f"{Color.HEADER}Explanation of Scores{Color.ENDC}\n")
    report_lines.append("The scores in this report have been centered using the Mean Rating (MRAT) correction method.")
    report_lines.append("This correction adjusts for individual differences in scale use by subtracting each individual's mean score across all 30 value items from their scores for each foundation.")
    report_lines.append("The centered scores represent the relative importance of each foundation within an individual's moral value system.")
    report_lines.append("Positive scores indicate foundations that are more important to the individual compared to their average foundation rating.")
    report_lines.append("Negative scores indicate foundations that are less important to the individual compared to their average foundation rating.")
    report_lines.append("Scores close to zero suggest foundations that are of average importance to the individual.")
    report_lines.append("The MRAT correction allows for more meaningful comparisons of moral foundation priorities across individuals and groups.")
    report_lines.append(f"{Color.OKBLUE}{'-' * 60}{Color.ENDC}\n")

    report = "\n".join(report_lines)

    if save_path:
        with open(save_path, 'w') as file:
            # Strip color codes for the file
            file.write(report.replace(Color.HEADER, '').replace(Color.OKBLUE, '').replace(Color.OKCYAN, '').replace(Color.OKGREEN, '').replace(Color.WARNING, '').replace(Color.FAIL, '').replace(Color.ENDC, '').replace(Color.BOLD, '').replace(Color.UNDERLINE, ''))
        print(f"\n{Color.OKCYAN}Report saved to {save_path}{Color.ENDC}")

    # Return the colored report for in-console display if needed
    return report