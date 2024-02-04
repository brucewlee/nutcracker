from typing import List, Optional
import random
#
from nutcracker.data.instance import Instance
from nutcracker.data.task import Task
#
#
class Pile:
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



    def __len__(self) -> int:
        """Return the number of Instances in the Pile.

        Args:
            None

        Raises:
            None

        Returns:
            int: Number of Instances in the Pile.
        """
        return len(self.instances)



    def __getitem__(self, index):
        """Return the Instance or a slice of Instances at the specified index.

        Args:
            index (int or slice): Index or slice of the Instance.

        Raises:
            IndexError: If the index is out of range.

        Returns:
            Instance or List[Instance]: The Instance or list of Instances at the given index.
        """
        if isinstance(index, int):
            # Handling single index
            if index >= len(self.instances) or index < 0:
                raise IndexError("Index out of range")
            return self.instances[index]
        elif isinstance(index, slice):
            # Handling slice object
            return self.instances[index]
        else:
            raise TypeError("Invalid argument type")



    def _ensure_consistent_construction(self) -> None:
        """
        Ensure all instances have the same construction type.
        
        Raises:
            ValueError: If instances have different construction types.
        
        Returns:
            None
        """
        if self.instances:
            constructions = {instance.config['construction'] for instance in self.instances}

            if len(constructions) > 1:
                error_msg = f"Detected constructions are: {', '.join(constructions)}"
                raise ValueError(error_msg)