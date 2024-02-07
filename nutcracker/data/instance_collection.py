from typing import Optional
import random
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



    def sample(
            self, 
            n: int, 
            seed: Optional[int] = None
        ) -> list:
        """Randomly sample 'n' instances from the collection.

        Args:
            n (int): The number of instances to sample.
            seed (Optional[int]): Optional random seed for reproducibility.

        Raises:
            ValueError: If 'n' is greater than the total number of instances.

        Returns:
            list: A list of 'n' randomly sampled instances.
        """
        if n > len(self.instances):
            raise ValueError("Sample size 'n' cannot be greater than the total number of instances.")
        if seed is not None:
            random.seed(seed)
        return random.sample(self.instances, n)
