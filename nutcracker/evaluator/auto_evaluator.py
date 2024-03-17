from typing import List, Union
import logging
#
from nutcracker.data.task import Task
from nutcracker.data.pile import Pile
from nutcracker.data.instance import MCQInstance
from nutcracker.data.instance import FRQInstance
from nutcracker.evaluator.mcq_evaluator import MCQEvaluator
from nutcracker.evaluator.frq_evaluator import FRQEvaluator
#
#
class AutoEvaluator:
    def __init__(self, data: Union[Pile, Task, List[MCQInstance], List[FRQInstance]], mcq_judge = 'recommended', frq_judge = 'recommended', **judge_kwargs) -> None:
        self.data = data
        self.judge_kwargs = judge_kwargs
        self._control_logging()
        self.frq_judge = frq_judge
        self.mcq_judge = mcq_judge

    def run(self, round_digits: int = 5) -> float:
        mcq_data = [instance for instance in self.data if isinstance(instance, MCQInstance)]
        frq_data = [instance for instance in self.data if isinstance(instance, FRQInstance)]
        self.logger.info(f"found {len(mcq_data)} MCQInstances.")
        self.logger.info(f"found {len(frq_data)} FRQInstances.")

        if mcq_data:
            mcq_evaluator = MCQEvaluator(mcq_data, judge=self.mcq_judge, **self.judge_kwargs)
            mcq_evaluator.run(round_digits)

        if frq_data:
            frq_evaluator = FRQEvaluator(frq_data, judge=self.frq_judge, **self.judge_kwargs)
            frq_evaluator.run(round_digits)

        # This function currently does not return accuracy. Modify as needed or use separate reporting.

    def _control_logging(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"AutoEvaluator created with {len(self.data)} instances.")
