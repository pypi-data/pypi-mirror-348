from typing import List, Tuple

def part_clip(lambda_: List[int]) -> List[int]:
    '''
    trims or removes trailing zeros from the list lambda.
    '''
    i = len(lambda_) - 1
    while i >= 0 and lambda_[i] == 0:
        i -= 1
    return lambda_[:i+1] if i >= 0 else []


def _is_non_increasing(part: List[int]):
    # Iterate through the list, comparing each element with the next one
    for i in range(len(part) - 1):
        # If the current element is smaller than the next one,
        # the list is not in descending order
        if part[i] < part[i + 1]:
            return False
    return True


def is_valid_part(part: List[int]) -> bool:
    if not isinstance(part, list):
        return False
    if not all(isinstance(x, int) for x in part):
        return False
    if not all(x >= 0 for x in part):
        return False
    if not _is_non_increasing(part):
        return False
    return True


class Partition:
    def __init__(self, partition: List[int]):
        if not is_valid_part(partition):
            raise ValueError("Invalid partition")
        self.partition = partition

    def __str__(self):
        return str(self.partition)

    def __repr__(self):
        return f"Partition({self.partition})"
    
    def draw(self):
        if len(self.partition) == 0:
            print("0")
            return
        
        for row in self.partition:
            print('[]' * row)

    def _max_rim_size(self) -> int:
        return sum(self.partition) + len(self.partition) - 1
    
    def is_in_range(self, nrow: int, ncol: int) -> bool:
        if nrow < 0 or ncol < 0:
            raise ValueError("nrow and ncol must be non-negative")
        
        if len(self.partition) == 0:
            return True
        
        if len(self.partition) > nrow:
            return False
        
        if self.partition[0] > ncol:
            return False
    
        return True

    def remove_rim_hooks(self, rim_size: int, acceptable_grid: Tuple[int, int]) -> Tuple['Partition', int, int]:
        """
        Removes rim hooks of a specified size from the partition to fit it within an acceptable grid,
        and counts the number of rim hooks removed along with their total height.

        Parameters:
        - rim_size: int
            The size of the rim hook to be removed.
        - acceptable_grid: Tuple[int, int]
            A tuple (nrow, ncol) representing the acceptable grid dimensions.

        Returns:
        - Tuple[Partition, int, int]
            A tuple containing:
            * the new partition after rim hook removal
            * the total number of rim hooks removed
            * the total height of rim hooks removed
        """
        if len(self.partition) == 0:
            return Partition([]), 0, 0
        if rim_size <= 0:
            return Partition(self.partition), 0, 0
        if rim_size > self._max_rim_size():
            return Partition([]), 0, 0

        nrow, ncol = acceptable_grid
        current_partition = self.partition.copy()  # Use a copy to avoid modifying the original partition
        total_rim_hooks_removed = 0  # Initialize the rim hook count
        
        while True:
            _partition = current_partition + [0]  # Append 0 to handle the difference calculation
            _rim_size = rim_size
            rim_hook_removed_this_iteration = False  # Flag to check if a rim hook was removed
        
            for i in range(len(_partition) - 1):
                delta = _partition[i] - _partition[i + 1]
                if delta >= _rim_size:
                    # Rim hook is entirely within a single row
                    _partition[i] -= _rim_size
                    _rim_size = 0
                    total_rim_hooks_removed += 1  # Increment the rim hook count
                    # Height of single-row rim hook is 0
                    rim_hook_removed_this_iteration = True
                    break
                if _partition[i + 1] > 0:
                    delta += 1
                _rim_size -= delta
                _partition[i] -= delta
                if _rim_size <= 0:
                    if _partition[i] < _partition[i+1]:
                        break
                    total_rim_hooks_removed += 1  # Increment the rim hook count
                    # Rim hook spans two rows, height = 1
                    rim_hook_removed_this_iteration = True
                    break


            if rim_hook_removed_this_iteration:
                # Accumulate the height of the removed rim hook
                if not _is_non_increasing(_partition):
                    # The partition is not valid after modification
                    return Partition([]), total_rim_hooks_removed, skew_partition_height([], self.partition)

                _partition = part_clip(_partition)
                new_partition = Partition(_partition)

                if new_partition.is_in_range(nrow, ncol):
                    # The new partition fits within the acceptable grid
                    return new_partition, total_rim_hooks_removed, skew_partition_height(new_partition.partition, self.partition)

                if new_partition.partition == current_partition:
                    # No further changes can be made; exit the loop
                    return Partition([]), total_rim_hooks_removed, skew_partition_height([], self.partition)

                # Update the partition for the next iteration
                current_partition = new_partition.partition
            else:
                # Unable to remove a rim hook of the specified size
                return 0, 0, 0




from typing import List

def skew_partition_height(lambda_partition: List[int], mu_partition: List[int]) -> int:
    """
    Calculates the height of the skew partition mu / lambda.
    
    The height is defined as the number of rows in the skew partition that contain at least one box.
    
    Parameters:
    - lambda_partition: List[int]
        The partition lambda, represented as a list of integers in non-increasing order.
    - mu_partition: List[int]
        The partition mu, represented as a list of integers in non-increasing order.
        It is assumed that lambda_partition is a subpartition of mu_partition.
    
    Returns:
    - int
        The height of the skew partition mu / lambda.
    
    Raises:
    - ValueError
        If lambda_partition is not contained within mu_partition.
    
    Example:
    >>> lambda_partition = [2]
    >>> mu_partition = [3, 1]
    >>> skew_partition_height(lambda_partition, mu_partition)
    2
    """

    if len(lambda_partition) == 0:
        return len(mu_partition)

    # Validation: Ensure lambda is contained within mu
    for i in range(len(lambda_partition)):
        if i >= len(mu_partition):
            raise ValueError("Partition lambda is not contained within partition mu (lambda has more rows).")
        if lambda_partition[i] > mu_partition[i]:
            raise ValueError(f"Partition lambda is not contained within partition mu (lambda[{i}] > mu[{i}]).")


    # Calculate the height of the skew partition
    height = 0
    for i in range(len(mu_partition)):
        mu_i = mu_partition[i]
        lambda_i = lambda_partition[i] if i < len(lambda_partition) else 0
        if mu_i > lambda_i:
            height += 1
    return height

    

    
if __name__ == "__main__":
    p = Partition([5, 5])
    p.remove_rim_hooks(rim_size=5, acceptable_grid=(2, 3))

    print(all_kstrict(2, 3, 5))