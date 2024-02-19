from typing import List, Optional
import random
import os
import logging
import glob
#
from nutcracker.data.instance import Instance
from nutcracker.data.task import Task
from nutcracker.data.instance_collection import InstanceCollection
#
#
import yaml
#
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
        #self._ensure_consistent_construction()



    @classmethod
    def load_from_db(cls, pile_name: str, db_directory: str):
        """Class method to initialize a Pile object from a pile name.

        Args:
            pile_name (str): The name of the pile, which corresponds to a YAML configuration file.
            db_directory (str): The local directory for the nutcracker database.

        Returns:
            Pile: An initialized Pile object containing tasks specified in the configuration.
        """
        cls.logger = logging.getLogger(__name__)
        library_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(library_dir, "data_config", "pile", f"{pile_name}.yaml")

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file for pile name '{pile_name}' not found at {config_path}")

        with open(config_path, 'r') as file:
            pile_config = yaml.safe_load(file)

        task_names = pile_config['task_name']
        tasks = []

        if ',' in task_names:
            # Specific tasks listed, load each by name
            for task_name in task_names.split(','):
                task_config_path = os.path.join(library_dir, "data_config", "task", f"{task_name}.yaml")
                task = Task.load_from_db(task_name, db_directory)
                tasks.append(task)
        else:
            # Pattern given, load all tasks matching the pattern
            for task_config_path in glob.glob(os.path.join(library_dir, "data_config", "task", f"{task_names}.yaml")):
                task_name = os.path.basename(task_config_path).replace('.yaml', '')
                task = Task.load_from_db(task_name, db_directory)
                tasks.append(task)

        # Initialize and return the Pile object with loaded tasks
        return cls(tasks=tasks)



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