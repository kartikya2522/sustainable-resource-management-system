from resources.water_resource import WaterResource
from resources.energy_resource import EnergyResource
from resources.waste_resource import WasteResource
from consumer.consumer import Consumer
from reports.sustainability_report import SustainabilityReport

def main():
    print("Welcome to the Sustainable Resource Management System Simulation\n")

    # 1. Create Resources
    print("--- Initializing Resources ---")
    water_res = WaterResource("Municipal Water", 1000.0, True)
    solar_res = EnergyResource("Solar Energy Grid", 5000.0, True)
    coal_res = EnergyResource("Coal Power Plant", 2000.0, False) # Non-renewable
    waste_res = WasteResource("Recyclable Waste", 500.0, False)

    all_resources = [water_res, solar_res, coal_res, waste_res]
    print("Resources initialized.\n")

    # 2. Create Consumers and Assign Resources
    print("--- Initializing Consumers ---")
    # Consumer 1: Eco-friendly household (Uses mostly renewable)
    c1 = Consumer(1, "Eco Household", [water_res, solar_res, waste_res])
    
    # Consumer 2: Industrial Factory (Uses heavy non-renewable)
    c2 = Consumer(2, "Industrial Factory", [water_res, coal_res])

    print("Consumers initialized.\n")

    # 3. Simulate Resource Consumption
    print("--- Simulating Resource Usage ---")
    
    # Valid Usage
    print("\n[Action] Eco Household using 50.0 Water...")
    c1.use_resource(water_res, 50.0)

    print("[Action] Eco Household using 200.0 Solar Energy...")
    c1.use_resource(solar_res, 200.0)

    print("[Action] Industrial Factory using 1800.0 Coal Power (High Usage)...")
    c2.use_resource(coal_res, 1800.0) # 1800/2000 = 90% (Should trigger alert later)

    print("[Action] Industrial Factory using 300.0 Water...")
    c2.use_resource(water_res, 300.0)

    # Invalid Usage Tests
    print("\n[Action] Eco Household trying to use Coal (Not Assigned)...")
    c1.use_resource(coal_res, 100.0)

    print("[Action] Industrial Factory trying to use -50 Water (Negative)...")
    c2.use_resource(water_res, -50.0)

    print("[Action] Industrial Factory trying to use 5000 Coal (Exceeds Limit)...")
    c2.use_resource(coal_res, 5000.0) # Only 200 left

    print("\nSimulation of usage completed.\n")

    # 4. Generate Reports
    print("--- Generating Consumer Reports ---")
    c1.generate_usage_report()
    c2.generate_usage_report()
    print("")

    # 5. Generate Sustainability Report
    report = SustainabilityReport(all_resources)
    report.generate_report()

if __name__ == "__main__":
    main()
