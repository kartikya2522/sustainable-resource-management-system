from resources.resource import Resource

class WasteResource(Resource):
    def __init__(self, name, total_available, renewable):
        """
        Initialize the WasteResource.
        """
        super().__init__(name, total_available, renewable)

    def report_usage(self):
        """
        Display current waste resource usage statistics.
        """
        print(f"--- Waste Resource Report ---")
        super().report_usage()
