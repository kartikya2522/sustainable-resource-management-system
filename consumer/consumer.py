from resources.resource import Resource

class Consumer:
    def __init__(self, consumer_id, name, assigned_resources=None):
        """
        Initialize the Consumer.

        Args:
            consumer_id (str or int): Unique identifier for the consumer.
            name (str): Name of the consumer.
            assigned_resources (list): List of Resource objects assigned to this consumer.
        """
        self.consumer_id = consumer_id
        self.name = name
        self.assigned_resources = assigned_resources if assigned_resources else []
        # Track usage per resource name internally to satisfy "Per-consumer consumption tracking"
        self._usage_history = {}

    def use_resource(self, resource, amount):
        """
        Use a specified amount of a resource if it is assigned to the consumer.

        Args:
            resource (Resource): The resource object to use.
            amount (float): The amount to consume.
        """
        if resource not in self.assigned_resources:
            print(f"Error: Resource '{resource.name}' is not assigned to Consumer '{self.name}'.")
            return

        if amount <= 0:
            print(f"Error: Invalid amount {amount} for resource '{resource.name}'. Amount must be positive.")
            return

        try:
            resource.update_availability(amount)
            
            # Track consumption internally
            if resource.name not in self._usage_history:
                self._usage_history[resource.name] = 0.0
            self._usage_history[resource.name] += amount

            print(f"Consumer '{self.name}' successfully used {amount:.2f} of '{resource.name}'.")
        except ValueError as e:
            print(f"Error using resource '{resource.name}': {e}")

    def generate_usage_report(self):
        """
        Display a summary of this consumer's resource usage.
        """
        print(f"--- Consumer Report: {self.name} (ID: {self.consumer_id}) ---")
        if not self.assigned_resources:
            print("No resources assigned.")
            return

        print("Consumption History:")
        if not self._usage_history:
            print("No resources consumed yet.")
        else:
            for res_name, amount in self._usage_history.items():
                print(f"  - {res_name}: {amount:.2f}")

        print("\nAssigned Resources Status (System Level):")
        for resource in self.assigned_resources:
            # We report the status of the resource itself
            resource.report_usage()
            print("") # Add a newline for readability
