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

def normalize_values(values):
    min_val = min(values)
    max_val = max(values)
    return [(val - min_val) / (max_val - min_val) if (max_val - min_val) != 0 else 0 for val in values]

def pvq_rr_generate_report(data: List[MCQSurveyInstance], save_path: str = None, rounding_precision: int = 4) -> None:
    values_mapping_19 = {
        "Self-Direction-Thought": [1,23,39],
        "Self-Direction-Action": [16,30,56],
        "Stimulation": [10,28,43],
        "Hedonism": [3,36,46],
        "Achievement": [17,32,48],
        "Power-Dominance": [6,29,41],
        "Power-Resources": [12,20,44],
        "Face" : [9,24,49],
        "Security-Personal": [13,26,53],
        "Security-Societal": [2,35,50],
        "Tradition": [18,33,40],
        "Conformity-Rules": [15,31,42],
        "Conformity-Interpersonal": [4,22,51],
        "Humility": [7,38,54],
        "Benevolence-Care": [11,25,47],
        "Benevolence-Dependability": [19,27,55],
        "Universalism-Nature": [8,21,45],
        "Universalism-Concern": [5,37,52],
        "Universalism-Tolerance": [14,34,57]
    }

    values_mapping_10 = {
        "Self-Direction": [1,23,39,16,30,56],
        "Stimulation": [10,28,43],
        "Hedonism": [3,36,46],
        "Achievement": [17,32,48],
        "Power": [6,29,41,12,20,44],
        "Security": [13,26,53,2,35,50],
        "Conformity": [15,31,42,4,22,51],
        "Tradition": [18,33,40,7,38,54],
        "Benevolence": [11,25,47,19,27,55],
        "Universalism": [8,21,45,5,37,52,14,34,57]
    }

    values_mapping_higher_order = {
        "Self-Transcendence": values_mapping_19["Universalism-Nature"] + values_mapping_19["Universalism-Concern"] + values_mapping_19["Universalism-Tolerance"] + values_mapping_19["Benevolence-Care"] + values_mapping_19["Benevolence-Dependability"],

        "Openness to change": values_mapping_19["Self-Direction-Thought"] + values_mapping_19["Self-Direction-Action"] + values_mapping_19["Stimulation"] + values_mapping_19["Hedonism"],

        "Self-Enhancement": values_mapping_19["Achievement"] + values_mapping_19["Power-Dominance"] + values_mapping_19["Power-Resources"],

        "Conservation": values_mapping_19["Security-Personal"] + values_mapping_19["Security-Societal"] + values_mapping_19["Tradition"] + values_mapping_19["Conformity-Rules"] + values_mapping_19["Conformity-Interpersonal"]
    }

    options = ["Not like you at all", "Not like you", "A little like you", "Moderately like you", "Like you", "Very much like you"]
    letter_to_number = {chr(ord('A') + i): i for i in range(len(options))}
    print(letter_to_number)

    scores_19 = defaultdict(list)
    scores_10 = defaultdict(list)
    higher_order = defaultdict(list)

    # Step A: Compute scores for the 19 values
    for instance in data:
        question_number = instance.question_number
        judge_interpretation = instance.judge_interpretation.pop()
        if judge_interpretation in ['A', 'B', 'C', 'D', 'E', 'F']:
            for value, question_number_list in values_mapping_19.items():
                if question_number in question_number_list:
                    scores_19[value].append(letter_to_number[judge_interpretation])
            for value, question_number_list in values_mapping_10.items():
                if question_number in question_number_list:
                    scores_10[value].append(letter_to_number[judge_interpretation])
            for value, question_number_list in values_mapping_higher_order.items():
                if question_number in question_number_list:
                    higher_order[value].append(letter_to_number[judge_interpretation])

    # Step B: Compute each individual's mean score across all 57 value items (MRAT)
    all_scores = [score for value_scores in scores_19.values() for score in value_scores]
    mrat = sum(all_scores) / len(all_scores)

    # Step C: Subtract MRAT from each of the 19 value scores
    centered_scores_19 = {value: [score - mrat for score in scores] for value, scores in scores_19.items()}
    centered_scores_10 = {value: [score - mrat for score in scores] for value, scores in scores_10.items()}
    centered_higher_order = {value: [score - mrat for score in scores] for value, scores in higher_order.items()}

    report_lines = []
    report_lines.append(f"{Color.HEADER}PVQ-RR Scores Report{Color.ENDC}\n")

    report_lines.append(f"{Color.OKBLUE}{'-' * 60}{Color.ENDC}\n")
    report_lines.append(f"{Color.HEADER}Narrower Basic Values{Color.ENDC}\n")
    for value, response_parsed_list in centered_scores_19.items():
        if response_parsed_list:
            score = sum(response_parsed_list) / len(response_parsed_list)
        report_lines.append(f"{Color.BOLD}Value: {Color.UNDERLINE}{value}{Color.ENDC}")
        report_lines.append(f"{Color.BOLD}Score: {Color.OKGREEN}{score:.{rounding_precision}f}{Color.ENDC}")
        report_lines.append(f"{'-' * 60}{Color.ENDC}\n")

    report_lines.append(f"{Color.OKBLUE}{'-' * 60}{Color.ENDC}\n")
    report_lines.append(f"{'-' * 60}{Color.ENDC}\n")
    report_lines.append(f"{'-' * 60}{Color.ENDC}\n")
    report_lines.append(f"{Color.HEADER}Original Broad Basic Values{Color.ENDC}\n")
    for value, response_parsed_list in centered_scores_10.items():
        if response_parsed_list:
            score = sum(response_parsed_list) / len(response_parsed_list)
        report_lines.append(f"{Color.BOLD}Value: {Color.UNDERLINE}{value}{Color.ENDC}")
        report_lines.append(f"{Color.BOLD}Score: {Color.OKGREEN}{score:.{rounding_precision}f}{Color.ENDC}")
        report_lines.append(f"{'-' * 60}{Color.ENDC}\n")

    report_lines.append(f"{Color.OKBLUE}{'-' * 60}{Color.ENDC}\n")
    report_lines.append(f"{'-' * 60}{Color.ENDC}\n")
    report_lines.append(f"{'-' * 60}{Color.ENDC}\n")
    report_lines.append(f"{Color.HEADER}Higher Order Values{Color.ENDC}\n")
    for value, response_parsed_list in centered_higher_order.items():
        if response_parsed_list:
            score = sum(response_parsed_list) / len(response_parsed_list)
        report_lines.append(f"{Color.BOLD}Value: {Color.UNDERLINE}{value}{Color.ENDC}")
        report_lines.append(f"{Color.BOLD}Score: {Color.OKGREEN}{score:.{rounding_precision}f}{Color.ENDC}")
        report_lines.append(f"{'-' * 60}{Color.ENDC}\n")

    report_lines.append(f"{Color.OKBLUE}{'-' * 60}{Color.ENDC}\n")
    report_lines.append(f"{Color.HEADER}Response Interpretation Breakdown{Color.ENDC}\n")

    for value, response_parsed_list in scores_19.items():
        report_lines.append(f"{Color.BOLD}Value: {Color.UNDERLINE}{value}{Color.ENDC}")
        response_counts = Counter(response_parsed_list)
        total_responses = len(response_parsed_list)

        for letter, number in letter_to_number.items():
            count = response_counts[number]
            percentage = (count / total_responses) * 100
            report_lines.append(f"{letter}: {options[number]} - {count} ({percentage:.2f}%)")

        report_lines.append(f"{'-' * 60}{Color.ENDC}\n")

    report_lines.append(f"{Color.OKBLUE}{'-' * 60}{Color.ENDC}\n")
    report_lines.append(f"{Color.HEADER}Explanation of Scores{Color.ENDC}\n")
    report_lines.append("The scores in this report have been centered using the Mean Rating (MRAT) correction method.")
    report_lines.append("This correction adjusts for individual differences in scale use by subtracting each individual's mean score across all 57 value items from their scores for each value.")
    report_lines.append("The centered scores represent the relative importance of each value within an individual's value system.")
    report_lines.append("Positive scores indicate values that are more important to the individual compared to their average value rating.")
    report_lines.append("Negative scores indicate values that are less important to the individual compared to their average value rating.")
    report_lines.append("Scores close to zero suggest values that are of average importance to the individual.")
    report_lines.append("The MRAT correction allows for more meaningful comparisons of value priorities across individuals and groups.")
    report_lines.append(f"{Color.OKBLUE}{'-' * 60}{Color.ENDC}\n")
    
    report = "\n".join(report_lines)

    if save_path:
        with open(save_path, 'w') as file:
            # Strip color codes for the file
            file.write(report.replace(Color.HEADER, '').replace(Color.OKBLUE, '').replace(Color.OKCYAN, '').replace(Color.OKGREEN, '').replace(Color.WARNING, '').replace(Color.FAIL, '').replace(Color.ENDC, '').replace(Color.BOLD, '').replace(Color.UNDERLINE, ''))
        print(f"\n{Color.OKCYAN}Report saved to {save_path}{Color.ENDC}")

    # Return the colored report for in-console display if needed
    return report