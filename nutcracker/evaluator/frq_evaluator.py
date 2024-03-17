from typing import List, Set, Optional, Union
import logging
#
from nutcracker.data.task import Task
from nutcracker.data.pile import Pile
from nutcracker.data.instance import FRQInstance
from nutcracker.utils import TqdmLoggingHandler
from nutcracker.evaluator.judges.frq_judge_alpha import FRQJudgeAlpha
from nutcracker.evaluator.judges.frq_judge_beta import FRQJudgeBeta
#
#
class FRQEvaluator:
    def __init__(
        self, data: Union[Pile, Task, List[FRQInstance]], judge: str = 'alpha', **judge_kwargs) -> None:
        self.data = data
        if judge == 'alpha' or judge == 'recommended':
            self.response_evaluator_judge = 'frq-judge-alpha'
            self.judge = FRQJudgeAlpha(**judge_kwargs)
        elif judge == 'beta' or judge == 'recommended':
            self.response_evaluator_judge = 'frq-judge-beta'
            self.judge = FRQJudgeBeta(**judge_kwargs)
        self._control_logging()



    def run(self, round_digits: int = 5) -> float:
        correct_count = 0
        for instance in TqdmLoggingHandler(self.data, logger=self.logger, desc="Processing Instances"):
            is_correct = self.judge.is_correct(instance)
            instance.response_correct = is_correct  # Update the instance attribute here
            instance.response_evaluator_judge = self.response_evaluator_judge # fingerprint
            if is_correct:
                correct_count += 1

        accuracy = correct_count / len(self.data) if len(self.data) > 0 else 0.0
        return round(accuracy, round_digits) 

    

    def _control_logging(
            self,
        ) -> None:
        """Control logging for Schema

        Args:
            None
        
        Raises:
            None
        
        Returns:
            None
        """
        self.logger = logging.getLogger(__name__)
        try:
            self.logger.info(f"runnable FRQEvaluator -> created with {len(self.data.instances)} instances.")
        except AttributeError:
            # happens when data is just a list of instances
            self.logger.info(f"runnable FRQEvaluator -> created with {len(self.data)} instances.")