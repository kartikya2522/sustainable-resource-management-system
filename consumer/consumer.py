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

        try:
            resource.update_availability(amount)
            # Since we cannot add new attributes, we don't track specific usage per consumer here
            # as per strict instructions "Do not add any extra methods or attributes."
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

        print("Assigned Resources Status:")
        for resource in self.assigned_resources:
            # We report the status of the resource itself
            resource.report_usage()
            print("") # Add a newline for readability
