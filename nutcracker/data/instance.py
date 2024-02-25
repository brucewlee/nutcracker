from typing import List
#
from nutcracker.utils import number_to_letter
#
#
class Instance:
    """Instance class for a task.
    The purpose of this class to allow switching between different Instance constructions while only interacting with the Instance class. 
    """
    @staticmethod
    def create_instance(
        config: dict,
        test_data: dict, 
        **kwargs
    ):
        """Factory method to create instances of different constructions.

        Args:
            config (dict): Configuration for the instance.
            test_data (dict): Test data for the instance.
            kwargs: Arbitrary keyword arguments. Expected to contain:
                MCQInstance:
                    example_data_list (List[dict], optional): List of example data.
        
        Raises:
            ValueError: If the instance construction is invalid.
        
        Returns:
            Instance: An instance of the specified construction.
        """
        if config['construction']['class'].lower().strip() == "mcq":
            # example_data_list can be empty for zero-shot evaluation
            example_data_list = kwargs.get('example_data_list')
            return MCQInstance(config, test_data, example_data_list)
        elif config['construction']['class'].lower().strip() == "frq":
            # example_data_list can be empty for zero-shot evaluation
            example_data_list = kwargs.get('example_data_list')
            return FRQInstance(config, test_data, example_data_list)
        else:
            raise ValueError("Invalid instance construction")



class MCQInstance(Instance):
    def __init__(
            self, 
            config: dict, 
            test_data: dict, 
            example_data_list: List[dict] = None
        ) -> None:
        """`MCQInstance` constructor.
        
        Args:
            config (dict): Configuration for the instance.
            test_data (dict): Test data for the instance.
            example_data_list (List[dict], optional): List of example data. Defaults to None.
            
        Raises:
            None

        Returns:
            None
        """
        # task-level attributes
        self.config = config
        self.example_data_list = example_data_list # not a list of Instance, just a list of dicts

        # below are attributes that are initialized from data
        self.centerpiece = test_data["centerpiece"]
        self.options = test_data["options"]
        self.correct_options = test_data["correct_options"]

        # Check if 'context' key exists in test_data
        self.context_exists = 'context' in test_data and test_data['context']
        if self.context_exists:
            self.context = test_data["context"]

        # below are derivational attributes that will be updated during code run
        self.user_prompt = self._format_user_prompt()
        self.model_response = None
        self.model_response_logprobs = None
        self.response_correct = False
        self.response_evaluator = None


    
    def _format_user_prompt(self) -> str:
        """Format the user prompt.

        Args:
            None

        Raises:
            ValueError: If the user prompt template is invalid.

        Returns:
            str: Formatted user prompt.
        """
        user_prompt = ""

        for key, value in self.config['user_prompt_template'].items():
            if value:
                # intercepting the wildcard declarations
                if value.startswith('<wild*card>'):
                    value = value.replace('<wild*card>', '')
                    
                    # Creating the complete function definition from YAML content
                    function_definition = f"def wildcard_formatter(centerpiece, options, correct_options, context=None):\n    {value}"

                    # Create the function dynamically
                    exec_globals = {}
                    exec(function_definition, exec_globals)
                    wildcard_formatter = exec_globals['wildcard_formatter']

                    if key == 'example':
                        for example_data in self.example_data_list[:self.config['few_shot']]:
                            user_prompt += wildcard_formatter(
                                context=example_data['context'],
                                centerpiece=example_data['centerpiece'],
                                options=example_data['options'],
                                correct_options=example_data['correct_options']
                            ) if self.context_exists else wildcard_formatter(
                                centerpiece=example_data['centerpiece'],
                                options=example_data['options'],
                                correct_options=example_data['correct_options']
                            )
                    else:
                        user_prompt += wildcard_formatter(
                            context=self.context,
                            centerpiece=self.centerpiece,
                            options=self.options,
                            correct_options=self.correct_options
                        ) if self.context_exists else wildcard_formatter(
                            centerpiece=self.centerpiece,
                            options=self.options,
                            correct_options=self.correct_options
                        )
                # if no wildcard, format normally
                else:
                    if key == 'example':
                        for example_data in self.example_data_list[:self.config['few_shot']]:
                            user_prompt += value.format(
                                context=example_data['context'],
                                centerpiece=example_data['centerpiece'],
                                options=example_data['options'],
                                correct_options=example_data['correct_options']
                            ) if self.context_exists else value.format(
                                centerpiece=example_data['centerpiece'],
                                options=example_data['options'],
                                correct_options=example_data['correct_options']
                            )                
                    else:
                        user_prompt += value.format(
                            context=self.context,
                            centerpiece=self.centerpiece,
                            options=self.options,
                            correct_options=self.correct_options
                        ) if self.context_exists else value.format(
                            centerpiece=self.centerpiece,
                            options=self.options,
                            correct_options=self.correct_options
                        )

        # if user prompt is empty, raise error
        if not user_prompt:
            raise ValueError("Invalid user prompt template")

        return user_prompt



class FRQInstance(Instance):
    def __init__(
            self, 
            config: dict, 
            test_data: dict, 
            example_data_list: List[dict] = None
        ) -> None:
        """`FRQInstance` constructor.
        
        Args:
            config (dict): Configuration for the instance.
            test_data (dict): Test data for the instance.
            example_data_list (List[dict], optional): List of example data. Defaults to None.
            
        Raises:
            None

        Returns:
            None
        """
        # task-level attributes
        self.config = config
        self.example_data_list = example_data_list # not a list of Instance, just a list of dicts

        # below are attributes that are initialized from data
        self.centerpiece = test_data["centerpiece"]
        self.correct_options = test_data["correct_options"]

        # below are derivational attributes that will be updated during code run
        self.user_prompt = self._format_user_prompt()
        self.model_response = None
        self.model_response_logprobs = None
        self.response_correct = False
        self.response_evaluator_engine = None


    
    def _format_user_prompt(self) -> str:
        """Format the user prompt.

        Args:
            None

        Raises:
            ValueError: If the user prompt template is invalid.

        Returns:
            str: Formatted user prompt.
        """
        user_prompt = ""

        for key, value in self.config['user_prompt_template'].items():
            if value:
                if key == 'example':
                    for example_data in self.example_data_list[:self.config['few_shot']]:
                        user_prompt += value.format(
                            centerpiece=example_data['centerpiece'],
                            correct_options=example_data['correct_options']
                        )                
                else:
                    user_prompt += value.format(
                        centerpiece=self.centerpiece,
                    )

        # if user prompt is empty, raise error
        if not user_prompt:
            raise ValueError("Invalid user prompt template")

        return user_prompt

