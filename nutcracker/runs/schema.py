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
        elif type(raw_response) == dict:
            if 'model_response' in raw_response:
                instance.model_response = raw_response['model_response']
            if 'model_response_logprobs' in raw_response:
                instance.model_response_logprobs = raw_response['model_response_logprobs']
            if 'user_prompt' in raw_response:
                instance.user_prompt = raw_response['user_prompt']



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