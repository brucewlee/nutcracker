from typing import List, Union
from collections import defaultdict
#
from nutcracker.data.instance import MCQInstance, FRQInstance
#
#
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

def generate_report(data: List[Union[MCQInstance, FRQInstance]], save_path: str = None, rounding_precision: int = 4) -> None:
    task_results = defaultdict(lambda: {'correct': 0, 'total': 0, 'details': None})
    total_correct = 0
    total_instances = 0

    for instance in data:
        task_name = instance.config['task_name']
        task_results[task_name]['total'] += 1
        task_results[task_name]['details'] = instance.config  # Assumes last instance config is representative
        if getattr(instance, 'response_correct', False):
            task_results[task_name]['correct'] += 1

    report_lines = []
    report_lines.append(f"{Color.HEADER}Accuracy Report by Task{Color.ENDC}\n")
    report_lines.append(f"{Color.OKBLUE}{'-' * 60}{Color.ENDC}\n")

    accuracies = []
    for task_name, results in task_results.items():
        accuracy_percentage = (results['correct'] / results['total']) * 100
        accuracies.append(accuracy_percentage)
        raw_accuracy = results['correct'] / results['total']
        details = results['details']
        construction = details.get('construction', {})
        few_shot = details.get('few_shot', 'N/A')
        language = details.get('language', 'N/A')
        
        # Handle construction class-specific wording
        if construction.get('class') == 'frq':
            construction_desc = f"Class: {Color.OKCYAN}frq (Free Response Questions)"
            construction_desc_2 = f"Style: {Color.OKCYAN}{construction.get('type', 'Unknown')}"
        elif construction.get('class') == 'mcq':
            construction_desc = f"Class: {Color.OKCYAN}mcq (Multiple Choice Questions)"
            construction_desc_2 = f"Choices: {Color.OKCYAN}{construction.get('n_choices', 'Unknown')}"
        else:
            construction_desc = "Unknown Construction"
            construction_desc_2 = "Unknown Construction"
        
        report_lines.append(f"{Color.BOLD}Task: {Color.UNDERLINE}{task_name}{Color.ENDC}")
        report_lines.append(f"{Color.BOLD}Construction: {Color.ENDC}")
        report_lines.append(f"{Color.BOLD}  - {construction_desc}{Color.ENDC}")
        report_lines.append(f"{Color.BOLD}  - {construction_desc_2}{Color.ENDC}")

        report_lines.append(f"{Color.BOLD}Few-shot: {Color.OKCYAN}{few_shot}{Color.ENDC}{Color.ENDC}")
        report_lines.append(f"{Color.BOLD}Language: {Color.OKCYAN}{language}{Color.ENDC}")
        report_lines.append(f"{Color.BOLD}{Color.OKGREEN}Correct: {results['correct']}/{results['total']} ({accuracy_percentage:.2f}%)")
        report_lines.append(f"{Color.BOLD}{Color.FAIL}Raw Accuracy: {raw_accuracy:.{rounding_precision}f}")
        report_lines.append(f"{'-' * 60}{Color.ENDC}\n")

    pile_average_accuracy = sum(accuracies) / len(accuracies) if accuracies else 0.0
    report_lines.append(f"{Color.BOLD}{Color.WARNING}Unique Tasks Found: {len(task_results)}{Color.ENDC}\n")
    report_lines.append(f"{Color.BOLD}{Color.WARNING}Average Accuracy: {pile_average_accuracy:.2f}%{Color.ENDC}\n")
    report = "\n".join(report_lines)

    # Optionally save to file
    if save_path:
        with open(save_path, 'w') as file:
            # Strip color codes for the file
            file.write(report.replace(Color.HEADER, '').replace(Color.OKBLUE, '').replace(Color.OKCYAN, '').replace(Color.OKGREEN, '').replace(Color.WARNING, '').replace(Color.FAIL, '').replace(Color.ENDC, '').replace(Color.BOLD, '').replace(Color.UNDERLINE, ''))
        print(f"\n{Color.OKCYAN}Report saved to {save_path}{Color.ENDC}")

    # Return the colored report for in-console display if needed
    return report


# To use this enhanced report generator, simply pass a list of MCQInstance objects along with an optional save path and rounding precision.
# generate_accuracy_report(data, save_path='accuracy_report.txt', rounding_precision=2)
