from typing import List, Set, Optional, Union
import logging
#
from nutcracker.data.task import Task
from nutcracker.data.pile import Pile
from nutcracker.data.instance import FRQInstance
from nutcracker.utils import TqdmLoggingHandler
from nutcracker.evaluator.engines.frq_engine_alpha import FRQEngineAlpha
#
#
class FRQEvaluator:
    def __init__(
        self, data: Union[Pile, Task, List[FRQInstance]], engine: str = 'alpha', **engine_kwargs) -> None:
        self.data = data
        if engine == 'alpha' or engine == 'recommended':
            self.response_evaluator_engine = 'frq-engine-alpha'
            self.engine = FRQEngineAlpha(**engine_kwargs)
        self._control_logging()



    def run(self, round_digits: int = 5) -> float:
        correct_count = 0
        for instance in TqdmLoggingHandler(self.data, logger=self.logger, desc="Processing Instances"):
            is_correct = self.engine.is_correct(instance)
            instance.response_correct = is_correct  # Update the instance attribute here
            instance.response_evaluator_engine = self.response_evaluator_engine # fingerprint
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