import numpy as np

class ConditionIndex:
    """
    Represents a quantitative measure of the current state or quality of a facility, system, or component.
    The index typically ranges from 1 to 99, with higher values indicating better condition and lower values indicating
    increasing levels of deterioration or need for maintenance. The ConditionIndex can be set directly or generated
    randomly according to predefined probability thresholds for realistic simulation. A threshold value (`DEGRADED_THRESHOLD`)
    is provided to help determine when a facility or system is considered "degraded" and may require maintenance or replacement.
    """

    DEGRADED_THRESHOLD: int = 25
    """int: The threshold value below which a condition index is considered "degraded".
    
    Facilities or systems with a condition index below this value are typically classified
    as requiring maintenance or replacement.
    """

    _value: float

    def __init__(self, value: float = None):
        """
        Initialize a ConditionIndex instance.

        Args:
          value (float, optional): The initial condition index value.
                                   If None, a random value will be generated using setRandom().
        """
        if value is not None:
            # ? Calls setter w/ validation per @property decorator below
            self.value = value
        else:
            self.setRandom()

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, index: float):
        """
        Sets the value of the condition index.

        Args:
          index (float): The value to set for the condition index. Must be greater than 0 and less than 100.

        Raises:
          ValueError: If the provided index is less than or equal to 0, or greater than or equal to 100.
        """
        if index >= 100:
            raise ValueError(
                f"Condition Index value: {index} is invalid. Value must be less than 100."
            )
        elif index <= 0:
            raise ValueError(
                f"Condition Index value: {index} is invalid. Value must be greater than 0."
            )
        self._value = index

    def setRandom(self):
        """
        Randomly assigns a value to the condition index based on predefined probability thresholds:

        - 7% chance to be set between 1 and 50 (representing a low condition index, degraded).
        - 88% chance to be set between 50 and 85 (representing average or good condition).
        - 5% chance to be set between 85 and 99.999 (representing excellent condition).

        This simulates the likelihood distribution of condition indices for facilities.
        """
        prob = np.random.rand()
        if prob < 0.07:  # 7% chance: below 50
            self._value = np.random.uniform(1, 50)
        elif prob < 0.07 + 0.88:  # 88% (1-0.07-0.05): between 50 and 85
            self._value = np.random.uniform(50, 85)
        else:  # 5% chance: above 85
            self._value = np.random.uniform(85, 99.999)

    def setRandomSeeded(self, seed: int):
        """
        Randomly assigns a value to the condition index based on predefined probability thresholds,
        using the provided seed for reproducibility.

        Args:
          seed (int): The seed to use for the random number generator.
        """
        rng = np.random.RandomState(seed)
        prob = rng.rand()
        if prob < 0.07:  # 7% chance: below 50
            self._value = rng.uniform(1, 50)
        elif prob < 0.07 + 0.88:  # 88% chance: between 50 and 85
            self._value = rng.uniform(50, 85)
        else:  # 5% chance: above 85
            self._value = rng.uniform(85, 99.999)

    def is_degraded(self) -> bool:
        """
        Determines if the condition index value indicates a degraded facility state.

        Returns:
            True if the condition index value is below the DEGRADED_THRESHOLD (default: 50.0), otherwise False.
        """
        return self._value < self.DEGRADED_THRESHOLD
