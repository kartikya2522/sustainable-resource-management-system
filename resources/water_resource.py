from resources.resource import Resource

class WaterResource(Resource):
    def __init__(self, name, total_available, renewable):
        """
        Initialize the WaterResource.
        """
        super().__init__(name, total_available, renewable)

    def report_usage(self):
        """
        Display current water usage statistics.
        """
        print(f"--- Water Resource Report ---")
        super().report_usage()
