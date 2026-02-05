from resources.resource import Resource

class EnergyResource(Resource):
    def __init__(self, name, total_available, renewable):
        """
        Initialize the EnergyResource.
        """
        super().__init__(name, total_available, renewable)

    def report_usage(self):
        """
        Display current energy usage statistics.
        """
        print(f"--- Energy Resource Report ---")
        super().report_usage()
