from typing import List, Set, Optional, Union
import logging
#
from nutcracker.data.task import Task
from nutcracker.data.pile import Pile
from nutcracker.data.instance import MCQInstance
from nutcracker.utils import TqdmLoggingHandler
from nutcracker.evaluator.judges.mcq_judge_alpha import MCQJudgeAlpha
from nutcracker.evaluator.judges.mcq_judge_beta import MCQJudgeBeta
from nutcracker.evaluator.judges.mcq_judge_gamma import MCQJudgeGamma
from nutcracker.evaluator.judges.mcq_judge_zeta import MCQJudgeZeta
#
#
class MCQEvaluator:
    def __init__(self, data: Union[Pile, Task, List[MCQInstance]], judge: str = 'alpha', **judge_kwargs) -> None:
        self.data = data
        if judge == 'alpha':
            self.response_evaluator_judge = 'mcq-judge-alpha'
            self.judge = MCQJudgeAlpha(**judge_kwargs)
        elif judge == 'beta':
            self.response_evaluator_judge = 'mcq-judge-beta'
            self.judge = MCQJudgeBeta(**judge_kwargs)
        elif judge == 'gamma':
            self.response_evaluator_judge = 'mcq-judge-gamma'
            self.judge = MCQJudgeGamma(**judge_kwargs)
        elif judge == 'zeta' or judge == 'recommended':
            self.response_evaluator_judge = 'mcq-judge-zeta'
            self.judge = MCQJudgeZeta(**judge_kwargs)
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
            self.logger.info(f"runnable MCQEvaluator -> created with {len(self.data.instances)} instances.")
        except AttributeError:
            # happens when data is just a list of instances
            self.logger.info(f"runnable MCQEvaluator -> created with {len(self.data)} instances.")