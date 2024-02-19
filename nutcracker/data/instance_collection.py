from typing import Optional
import random
import pickle
#
class InstanceCollection:
    def __init__(self) -> None:
        """Initialize an empty collection of instances."""
        self.instances = []



    def __len__(self) -> int:
        """Return the number of instances in the collection.

        Returns:
            int: The total number of instances in the collection.
        """
        return len(self.instances)



    def __getitem__(self, index):
        """Retrieve specific instance(s) by index or slice.

        Args:
            index (int or slice): The index of the instance to retrieve or a slice object to get a range of instances.

        Raises:
            IndexError: If the index is out of range.
            TypeError: If the provided index is not an int or slice.

        Returns:
            Instance or list of Instances: A single instance or a list of instances based on the provided index.
        """
        if isinstance(index, int):
            if index >= len(self.instances) or index < 0:
                raise IndexError("Index out of range")
            return self.instances[index]
        elif isinstance(index, slice):
            return self.instances[index]
        else:
            raise TypeError("Invalid argument type")



    def sample(self, n: int, seed: Optional[int] = None, in_place: bool = False) -> Optional[list]:
        """
        Randomly sample 'n' instances from the collection. Optionally modify the collection in place.

        Args:
            n (int): The number of instances to sample.
            seed (Optional[int]): Optional random seed for reproducibility.
            in_place (bool): If True, the collection itself is modified to only contain the sampled instances.

        Raises:
            ValueError: If 'n' is greater than the total number of instances.

        Returns:
            list or None: A list of 'n' randomly sampled instances if in_place is False. None if in_place is True.
        """
        if n > len(self.instances):
            raise ValueError("Sample size 'n' cannot be greater than the total number of instances.")
        if seed is not None:
            random.seed(seed)
        sampled_indices = random.sample(range(len(self.instances)), n)

        if in_place:
            self.instances = [self.instances[i] for i in sampled_indices]
            return None
        else:
            return [self.instances[i] for i in sampled_indices]



    def get_max_token_length_user_prompt(self) -> int:
        """Find the maximum user prompt length across all instances.

        Returns:
            int: The maximum length of user prompts in the collection.
        """
        max_length = 0
        for instance in self.instances:
            prompt_length = len(instance.user_prompt) 
            prompt_length_tokens = prompt_length // 4
            max_length = max(max_length, prompt_length_tokens)
        return max_length

    

    def save_to_file(self, file_path: str) -> None:
        """Save the current object to a file using pickle.

        Args:
            file_path (str): The path where the object should be saved.
        """
        with open(file_path, 'wb') as file:
            pickle.dump(self, file)



    @classmethod
    def load_from_file(cls, file_path: str) -> 'InstanceCollection':
        """Load an object from a file.

        Args:
            file_path (str): The path to the file from which to load the object.

        Returns:
            InstanceCollection: The loaded object.
        """
        with open(file_path, 'rb') as file:
            obj = pickle.load(file)
        if not isinstance(obj, cls):
            raise TypeError(f"The loaded object is not of type {cls.__name__}")
        return obj