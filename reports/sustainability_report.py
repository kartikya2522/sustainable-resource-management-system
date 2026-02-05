class SustainabilityReport:
    def __init__(self, resources):
        """
        Initialize the SustainabilityReport.

        Args:
            resources (list): List of Resource objects to report on.
        """
        self.resources = resources

    def generate_report(self):
        """
        Generates a text-based sustainability report including usage stats,
        alerts, and recommendations.
        """
        print("==========================================")
        print("      SUSTAINABILITY REPORT GENERATED     ")
        print("==========================================")

        total_usage = 0.0
        renewable_usage = 0.0
        non_renewable_usage = 0.0
        alerts = []

        print("\n--- Individual Resource Usage ---")
        for resource in self.resources:
            # Calculate usage
            # Note: Accessing _current_available directly as per Python conventions for this scope,
            # ensuring we don't modify the Resource class to add getters if not present.
            used_amount = resource.total_available - resource._current_available
            usage_percent = (used_amount / resource.total_available) * 100 if resource.total_available > 0 else 0
            
            total_usage += used_amount
            if resource.renewable:
                renewable_usage += used_amount
            else:
                non_renewable_usage += used_amount

            print(f"{resource.name}: Used {used_amount:.2f} of {resource.total_available:.2f} ({usage_percent:.1f}%)")

            if usage_percent > 80:
                alerts.append(f"CRITICAL: {resource.name} usage is at {usage_percent:.1f}% (Threshold: 80%)")

        print("\n--- Usage Summary ---")
        print(f"Total Resource Usage: {total_usage:.2f}")
        print(f"Renewable Usage: {renewable_usage:.2f}")
        print(f"Non-Renewable Usage: {non_renewable_usage:.2f}")

        if alerts:
            print("\n--- Alerts ---")
            for alert in alerts:
                print(alert)
        else:
            print("\n--- Alerts ---")
            print("No critical resource usage detected.")

        print("\n--- Sustainability Recommendations ---")
        if non_renewable_usage > renewable_usage:
            print("- Shift consumption towards renewable resources.")
        
        if alerts:
            print("- Immediate conservation measures required for critical resources.")
        else:
            print("- Maintain current consumption patterns.")
            
        if total_usage == 0:
            print("- No resources have been used yet.")
        
        print("\n==========================================")
