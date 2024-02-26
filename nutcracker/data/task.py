from typing import Optional
import json
import os
import logging
import glob
#
from nutcracker.data.instance import Instance
from nutcracker.data.instance_collection import InstanceCollection
#
#
import yaml
#
#
#
class Task(InstanceCollection):
    def __init__(
            self, 
            test_path: str,
            config_path: Optional[str] = None, 
            example_path: Optional[str] = None,
            override_config: Optional[dict] = None,
        ) -> None:
        """Initialize a task object.

        Args:
            config_path (Optional[str], optional): Path to the config file. Defaults to None.
            test_path (Optional[str], optional): Path to the test file. Defaults to None.
            example_path (Optional[str], optional): Path to the example file. Defaults to None.
            override_config (Optional[dict], optional): User-given config. Defaults to None.
        
        Raises:
            ValueError: If there are no instances either by directly giving as input or through test_path.
        
        Returns:
            None
        """
        self.config = {}
        self.instances = []
        self.example_data_list = []

        # load config if config path is given
        if config_path is not None:
            self._load_config(config_path)
        # override config if params are given
        self._override(override_config)
        # populate self.instances
        self._load_data(test_path, example_path)
        # check validity of this Task object
        self._check_validity()

        self.logger = logging.getLogger(__name__)



    @classmethod
    def load_from_db(cls, task_name: str, db_directory: str, **kwargs):
        """(Not Supported due to Cloud Computing Restrictions) Class method to initialize a Task object from a task ID.

        Args:
            task_name (str): The task name, e.g., 'mmlu-abstract-algebra'.
            db_directory (str): The local directory for nutcracker db.

        Returns:
            Task: An initialized Task object.
        """
        cls.logger = logging.getLogger(__name__)
        # Determine the directory of the current script in the library
        library_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to the config file relative to the library directory
        config_path = os.path.join(library_dir, "data_config", "task", f"{task_name}.yaml")
        #print(config_path)
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file for task name '{task_name}' not found at {config_path}")
        # Load task config
        with open(config_path, 'r') as file:
            task_config = yaml.safe_load(file)

        # Check if task name directory exists in DB
        local_task_path = os.path.join(db_directory, task_name)
        if not os.path.exists(local_task_path):
            raise FileNotFoundError(f"DB task directory for task name '{task_name}' not found at '{local_task_path}'")
        cls.logger.info(f"Successfully located and checked '{local_task_path}' for '{task_name}'")


        test_path, example_path, config_path = None, None, None
        for file_key, file_name in task_config['filename'].items():
            local_file_path = os.path.join(local_task_path, file_name)
            if file_key == 'test':
                test_path = local_file_path
            elif file_key == 'dev':
                example_path = local_file_path
            elif file_key == 'config':
                config_path = local_file_path

        # Initialize and return the Task object
        return cls(test_path=test_path, example_path=example_path, config_path=config_path, **kwargs)
    


    def _load_config(
            self, 
            config_path: str
        ) -> None: 
        """Load the config file.

        Args:
            config_path (str): Path to the config file.
        
        Raises:
            None
        
        Returns:
            None
        """
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)



    def _load_data(
            self, 
            test_path: str,
            example_path: Optional[str] = None
        ) -> None:
        """Load the test / example file.

        Args:
            test_path (str): Path to the test / example file.
            example_path (Optional[str], optional): Path to the example file. Defaults to None.
        
        Raises:
            None
        
        Returns:
            None
        """
        # if example path is given, load the example file for few-shot
        if example_path is not None:
            with open(example_path, 'r') as file:
                for line in file:
                    self.example_data_list.append(json.loads(line))

        # load the test file
        with open(test_path, 'r') as file:
            for line in file:
                test_data = json.loads(line)
                instance = Instance.create_instance(
                    config = self.config, 
                    test_data = test_data,
                    example_data_list = self.example_data_list
                )
                self.instances.append(instance)



    def _override(
            self,
            override_config: Optional[dict] = None,
        ) -> None:
        """Override the config from path using user-given config.

        Args:
            override_config (Optional[dict], optional): User-given config. Defaults to None.

        Raises:
            None
        
        Returns:
            None
        """
        if override_config:
            for key, value in override_config.items():
                self.config[key] = value
    


    def _check_validity(self) -> None:
        """Check validity of the Task object.
        
        Args:
            None
        
        Raises:
            ValueError: If there are no test instances.
            ValueError: If there is no config.
            ValueError: If number of few-shot examples is larger than the number of examples available.
            ValueError: If config is missing necessary keys.
        
        Returns:
            None
        """
        # check if instances is empty and raise an error if so
        if not self.instances:
            raise ValueError("No test instances available. Please provide test instances or a valid test path.")
        
        # check if config is empty and raise an error if so
        if not self.config:
            raise ValueError("No config available. Please provide a valid config path.")
        
        # check if number of few-shot is smaller than length of examples
        if self.config['few_shot'] > len(self.example_data_list):
            #print(len(self.example_data_list))
            raise ValueError("Number of few-shot examples is larger than the number of examples available.")
        
        # check if config contains all necessary keys
        necessary_keys = ['task_name', 'construction', 'user_prompt_template', 'few_shot']
        for key in necessary_keys:
            if key not in self.config:
                raise ValueError("Config is missing necessary {} key".format(key))
    


    @staticmethod
    def list_all() -> list:
        """
        List all available task names based on the YAML configuration files in the data_config/task directory.

        Args:
            data_config_directory (str): The path to the data_config directory containing task configurations.

        Returns:
            list: A list of task names available in the data_config/task directory.
        """
        # Determine the directory of the current script in the library
        library_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the path to the config file relative to the library directory
        config_path = os.path.join(library_dir, "data_config")

        # Construct the path to the task configurations directory
        tasks_config_path = os.path.join(config_path, "task")
        
        # Use glob to find all YAML files in the directory
        task_config_files = glob.glob(os.path.join(tasks_config_path, "*.yaml"))
        
        # Extract the task names from the filenames
        task_names = [os.path.basename(filename).replace('.yaml', '') for filename in task_config_files]
        
        return task_names