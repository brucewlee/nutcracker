from typing import Optional
import json
import os
import logging
#
from nutcracker.data.instance import Instance
#
#
from huggingface_hub import hf_hub_download
import yaml
#
#
#
class Task:
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
    def load_from_db(cls, task_name: str, db_directory: str):
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
        print(config_path)
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
        return cls(test_path=test_path, example_path=example_path, config_path=config_path)



    @classmethod
    def load_from_id(cls, task_id: str, user_given_directory: str):
        """(Not Supported due to Cloud Computing Restrictions) Class method to initialize a Task object from a task ID.

        Args:
            task_id (str): The task ID, e.g., 'mmlu-abstract-algebra'.
            user_given_directory (str): The local directory to save the downloaded files.

        Returns:
            Task: An initialized Task object.
        """
        cls.logger = logging.getLogger(__name__)
         # Determine the directory of the current script in the library
        library_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the path to the config file relative to the library directory
        config_path = os.path.join(library_dir, "data_config", "task", f"{task_id}.yaml")

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file for task ID '{task_id}' not found at {config_path}")
        
        # Load task config
        with open(config_path, 'r') as file:
            task_config = yaml.safe_load(file)

        repo_id = task_config['repo_id']
        local_task_path = os.path.join(user_given_directory, task_id)

        # Ensure local task directory exists
        if not os.path.exists(local_task_path):
            os.makedirs(local_task_path)
        
        example_path = None
        # Download files from Hugging Face if they don't exist locally
        #test_path, example_path, config_path = None, None, None
        for file_key, file_name in task_config['filename'].items():
            local_file_path = os.path.join(local_task_path, file_name)
            if not os.path.exists(local_file_path):
                hf_hub_download(
                    repo_id=repo_id, 
                    repo_type=task_config['repo_type'],
                    revision='main',
                    filename=file_name, 
                    local_dir=local_task_path,
                    local_dir_use_symlinks=False
                )
                cls.logger.info(f"Downloaded {file_name} to {local_file_path}")
            else:
                cls.logger.info(f"File {file_name} already exists at {local_file_path}")

            if file_key == 'test':
                test_path = local_file_path
            elif file_key == 'dev':
                example_path = local_file_path
            elif file_key == 'config':
                config_path = local_file_path

        # Initialize and return the Task object
        return cls(test_path=test_path, example_path=example_path, config_path=config_path)



    def __len__(self) -> int:
        """Return the number of instances in the task.

        Args:
            None
        
        Raises:
            None
        
        Returns:
            int: Number of test instances in the task.
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
            print(len(self.example_data_list))
            raise ValueError("Number of few-shot examples is larger than the number of examples available.")
        
        # check if config contains all necessary keys
        necessary_keys = ['task_name', 'construction', 'user_prompt_template', 'few_shot']
        for key in necessary_keys:
            if key not in self.config:
                raise ValueError("Config is missing necessary {} key".format(key))
    


