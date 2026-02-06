from fastapi import FastAPI, HTTPException
import sys
import os

# Ensure the parent directory is in the path to import from sibling modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from resources.water_resource import WaterResource
from resources.energy_resource import EnergyResource
from resources.waste_resource import WasteResource
from consumer.consumer import Consumer
from api.external_climatiq_api import get_carbon_emissions

app = FastAPI(title="Sustainable Resource Management API")

# --- System State Setup (Simulated Database) ---
# Recreating the simulation environment
water_res = WaterResource("Municipal Water", 1000.0, True)
solar_res = EnergyResource("Solar Energy Grid", 5000.0, True)
coal_res = EnergyResource("Coal Power Plant", 2000.0, False)
waste_res = WasteResource("Recyclable Waste", 500.0, False)

all_resources = [water_res, solar_res, coal_res, waste_res]

# Initialize Consumers
c1 = Consumer(1, "Eco Household", [water_res, solar_res, waste_res])
c2 = Consumer(2, "Industrial Factory", [water_res, coal_res])

# Simulate some initial usage to make the report interesting
c1.use_resource(water_res, 50.0)
c1.use_resource(solar_res, 200.0)
c2.use_resource(coal_res, 1800.0) # High usage
c2.use_resource(water_res, 300.0)

@app.get("/sustainability/context")
def get_sustainability_context():
    """
    Returns a combined report of internal system sustainability metrics
    and external carbon emission context from Climatiq.
    """
    try:
        # 1. Calculate Internal Metrics
        # Manually calculating as per SustainabilityReport logic to return JSON
        total_usage = 0.0
        renewable_usage = 0.0
        non_renewable_usage = 0.0
        resource_stats = []
        alerts = []

        for resource in all_resources:
            # Calculate usage (total_available - current_available)
            # Accessing protected member _current_available as in the Report class
            used_amount = resource.total_available - resource._current_available
            usage_percent = (used_amount / resource.total_available) * 100 if resource.total_available > 0 else 0
            
            total_usage += used_amount
            if resource.renewable:
                renewable_usage += used_amount
            else:
                non_renewable_usage += used_amount

            resource_stats.append({
                "name": resource.name,
                "used": round(used_amount, 2),
                "total": round(resource.total_available, 2),
                "usage_percent": round(usage_percent, 1),
                "renewable": resource.renewable
            })

            if usage_percent > 80:
                alerts.append(f"CRITICAL: {resource.name} usage is at {usage_percent:.1f}%")

        internal_metrics = {
            "total_resource_usage": round(total_usage, 2),
            "renewable_usage": round(renewable_usage, 2),
            "non_renewable_usage": round(non_renewable_usage, 2),
            "resource_breakdown": resource_stats,
            "alerts": alerts,
            "recommendation": "Shift consumption towards renewable resources." if non_renewable_usage > renewable_usage else "Maintain current consumption patterns."
        }

        # 2. Fetch External Context
        # Using the total energy usage (Solar + Coal) from our internal state
        total_energy_kwh = 0.0
        # Identifying energy resources by type check or name assumption for this simulation
        for res in all_resources:
            if isinstance(res, EnergyResource):
                used = res.total_available - res._current_available
                total_energy_kwh += used

        external_data = None
        external_error = None
        
        try:
            # Fetch for US region as default context
            external_data = get_carbon_emissions(total_energy_kwh, region="US")
            if external_data is None:
                external_error = "External API returned no data (check API key)."
        except Exception as e:
            external_error = f"Failed to connect to external API: {str(e)}"

        # 3. Construct Combined Response
        response = {
            "internal_sustainability_metrics": internal_metrics,
            "external_carbon_context": {
                "description": f"Carbon emission estimate for total energy usage ({total_energy_kwh} kWh) in US region.",
                "data": external_data,
                "status": "success" if external_data else "partial_failure",
                "error": external_error
            }
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Make sure to allow running via uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
