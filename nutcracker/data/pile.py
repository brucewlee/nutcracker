from typing import List, Optional
import random
#
from nutcracker.data.instance import Instance
from nutcracker.data.task import Task
from nutcracker.data.instance_collection import InstanceCollection
#
#
class Pile (InstanceCollection):
    def __init__(
            self,
            tasks: List[Task],
            shuffle: bool = False,
            shuffle_seed: Optional[int] = None
        ) -> None:
        """Initialize a Pile object with a list of Task objects.

        Args:
            tasks (List[Task]): A list of Task objects.
            shuffle (bool): If True, shuffle the instances.
            shuffle_seed (Optional[int]): Seed for shuffling. Defaults to None.

        Raises:
            None

        Returns:
            None
        """
        self.instances = []
        for task in tasks:
            self.instances.extend(task.instances)

        if shuffle:
            if shuffle_seed is not None:
                random.seed(shuffle_seed)
            random.shuffle(self.instances)
        self._ensure_consistent_construction()



    def add_instance(
            self, 
            instance: Instance
        ) -> None:
        """Add an Instance to the Pile.

        Args:
            instance (Instance): The Instance object to add.

        Raises:
            None

        Returns:
            None
        """
        self.instances.append(instance)
        self._ensure_consistent_construction()



    def add_task(
            self, 
            task: Task
        ) -> None:
        """Add a Task to the Pile.

        Args:
            task (Task): The Task object to add.
        
        Raises:
            None
        
        Returns:
            None
        """
        self.instances.extend(task.instances)
        self._ensure_consistent_construction()



    def _ensure_consistent_construction(self) -> None:
        """
        Ensure all instances have the same construction type.
        
        Raises:
            ValueError: If instances have different construction types.
        
        Returns:
            None
        """
        if self.instances:
            constructions = {instance.config['construction']['class'] for instance in self.instances}

            if len(constructions) > 1:
                error_msg = f"Detected constructions are: {', '.join(constructions)}"
                raise ValueError(error_msg)