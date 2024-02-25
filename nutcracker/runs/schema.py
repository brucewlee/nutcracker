from typing import Union, List, Dict, Optional
import logging
#
from nutcracker.data.instance import Instance
from nutcracker.data.task import Task
from nutcracker.data.pile import Pile
from nutcracker.utils import TqdmLoggingHandler
#
#
class Schema:
    def __init__(
        self, 
        model: object, 
        data: Union[Instance, Task, Pile, List[Instance]], 
        other_params: Optional[Dict] = None
    ) -> None:
        """Initialize a Schema object.
        """
        self.model = model
        self.other_params = other_params or {}
        self.instances = self._extract_instances(data)
        self.source_tasks = set(instance.config['task_name'] for instance in self.instances)
        self._control_logging()



    def _extract_instances(
            self, 
            data: Union[Instance, Task, Pile, List[Instance]]
        ) -> List[Instance]:
        """Extract instances from the provided data.

        Args:
            data (Union[Instance, Task, Pile, List[Instance]]): The data to extract instances from.

        Raises:
            ValueError: If the data type is not recognized.

        Returns:
            List[Instance]: A list of Instance objects.
        """
        instances = []

        if isinstance(data, Instance):
            instances.append(data)
        elif isinstance(data, Task):
            instances.extend(data.instances)
        elif isinstance(data, Pile):
            instances.extend(data.instances)
        elif isinstance(data, list) and all(isinstance(item, Instance) for item in data):
            instances.extend(data)
        else:
            raise ValueError("Unsupported data type for Schema")

        return instances
    


    def _single_call(self, instance):
        raw_response = self.model.respond(instance.user_prompt)
        if type(raw_response) == str:
            instance.model_response = raw_response
        elif type(raw_response) == tuple:
            # model_response expects a string
            # " B. A defendant was home in ... him to death."
            instance.model_response = raw_response[0]
            # model_response_logprobs expects a list of list of tuples (with first item string text and second item logprobs, any following values in the tuple is ignored)
            #[[('D', -1.4479486, '23.51%'), ('A', -1.7440797, '17.48%'), ('C', -2.0701218, '12.62%'), (' D', -2.214632, '10.92%'), (' A', -2.2270546, '10.78%')], [('.', -0.0070102946, '99.3%'), ('<|end|>', -5.1865225, '0.56%'), (' -', -7.4769926, '0.06%'), (' ', -8.7467, '0.02%'), ('-', -9.260667, '0.01%')], [(' A', -0.016997492, '98.31%'), (' In', -4.900506, '0.74%'), (' The', -4.9796934, '0.69%'), ('<|end|>', -6.92834, '0.1%'), (' ', -7.4558744, '0.06%')], [(' defendant', -0.0001008015, '99.99%'), ('.', -9.534555, '0.01%'), (' victim', -11.806505, '0.0%'), (' situation', -12.522846, '0.0%'), (' ', -12.812527, '0.0%')], ... [(' death', -1.147242e-06, '100.0%'), (' de', -15.059201, '0.0%'), (' ', -15.463262, '0.0%'), ('death', -15.720479, '0.0%'), (' the', -15.74908, '0.0%')], [('.', -4.143808e-05, '100.0%'), ('.\n', -10.252204, '0.0%'), ('.\n\n', -12.5602455, '0.0%'), ('<|end|>', -14.175714, '0.0%'), ('."', -14.577833, '0.0%')]]
            instance.model_response_logprobs = raw_response[1]



    def run(
            self,
        ) -> None:
        """Run the schema.

        Args:
            None

        Raises:
            None

        Returns:
            None
        """
        if self.logger.getEffectiveLevel() <= logging.INFO:
            for instance in TqdmLoggingHandler(self.instances, logger=self.logger, desc="Processing Instances"):
                self._single_call(instance)
        else:
            for instance in self.instances:
                self._single_call(instance)



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
        self.logger.info(f"runnable Schema -> created with {len(self.instances)} instances from {self.source_tasks}.")