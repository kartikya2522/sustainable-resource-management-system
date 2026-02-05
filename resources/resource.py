class Resource:
    def __init__(self, name, total_available, renewable):
        """
        Initialize the Resource.

        Args:
            name (str): Name of the resource.
            total_available (float): Total amount of resource available.
            renewable (bool): Whether the resource is renewable.
        """
        self.name = name
        self.total_available = float(total_available)
        self.renewable = renewable
        self._current_available = self.total_available

    def report_usage(self):
        """
        Display current usage statistics of the resource (used vs available).
        """
        used = self.total_available - self._current_available
        print(f"Resource: {self.name}")
        print(f"Total Available: {self.total_available:.2f}")
        print(f"Current Available: {self._current_available:.2f}")
        print(f"Used: {used:.2f}")

    def update_availability(self, amount):
        """
        Reduce the available amount when the resource is used.

        Args:
            amount (float): The amount of resource to consume.

        Raises:
            ValueError: If amount is not positive or exceeds available resource.
        """
        if amount <= 0:
            raise ValueError(f"Usage amount must be positive. Received: {amount}")
        
        if amount > self._current_available:
            raise ValueError(f"Requested amount {amount} exceeds available resource {self._current_available} for '{self.name}'.")

        self._current_available -= amount
