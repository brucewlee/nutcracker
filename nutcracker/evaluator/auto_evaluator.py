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
    def __init__(self, data: Union[Pile, Task, List[MCQInstance], List[FRQInstance]], mcq_engine = 'recommended', frq_engine = 'recommended', **engine_kwargs) -> None:
        self.data = data
        self.engine_kwargs = engine_kwargs
        self._control_logging()
        self.frq_engine = frq_engine
        self.mcq_engine = mcq_engine

    def run(self, round_digits: int = 5) -> float:
        mcq_data = [instance for instance in self.data if isinstance(instance, MCQInstance)]
        frq_data = [instance for instance in self.data if isinstance(instance, FRQInstance)]
        self.logger.info(f"found {len(mcq_data)} MCQInstances.")
        self.logger.info(f"found {len(frq_data)} FRQInstances.")

        if mcq_data:
            mcq_evaluator = MCQEvaluator(mcq_data, engine=self.mcq_engine, **self.engine_kwargs)
            mcq_evaluator.run(round_digits)

        if frq_data:
            frq_evaluator = FRQEvaluator(frq_data, engine=self.frq_engine, **self.engine_kwargs)
            frq_evaluator.run(round_digits)

        # This function currently does not return accuracy. Modify as needed or use separate reporting.

    def _control_logging(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"AutoEvaluator created with {len(self.data)} instances.")
