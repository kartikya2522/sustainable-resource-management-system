from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sys
import os

# Ensure the parent directory is in the path to import from sibling modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from resources.water_resource import WaterResource
from resources.energy_resource import EnergyResource
from resources.waste_resource import WasteResource
from consumer.consumer import Consumer

app = FastAPI(title="Sustainable Resource Management API")

# Setup templates directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Mount static files
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

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

# Internal Carbon Intensity Factors (kg CO2e per unit)
# These are estimated values for the simulation
CARBON_FACTORS = {
    "Municipal Water": 0.001,    # Pumping/Treatment
    "Solar Energy Grid": 0.05,   # Lifecycle emissions
    "Coal Power Plant": 0.9,     # Direct emissions
    "Recyclable Waste": 0.02     # Transport/Processing
}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Serves the landing page.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/sustainability/context")
def get_sustainability_context():
    """
    Returns a combined report of internal system sustainability metrics.
    Now calculates environmental impact internally without external APIs.
    """
    try:
        # 1. Calculate Internal Metrics
        total_usage = 0.0
        renewable_usage = 0.0
        non_renewable_usage = 0.0
        resource_stats = []
        alerts = []
        
        # Environmental Impact Calculation
        total_carbon_footprint = 0.0

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

            # Calculate Carbon Footprint for this resource
            factor = CARBON_FACTORS.get(resource.name, 0.0)
            emissions = used_amount * factor
            total_carbon_footprint += emissions

            resource_stats.append({
                "name": resource.name,
                "used": round(used_amount, 2),
                "total": round(resource.total_available, 2),
                "usage_percent": round(usage_percent, 1),
                "renewable": resource.renewable,
                "emissions": round(emissions, 2)
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

        # 2. Environmental Impact Report (Internal Logic Only)
        impact_report = {
            "description": "Estimated carbon footprint based on internal resource usage and type intensity factors.",
            "total_co2e": round(total_carbon_footprint, 2),
            "unit": "kg CO2e",
            "status": "simulated_internal"
        }

        # 3. Construct Combined Response
        response = {
            "internal_sustainability_metrics": internal_metrics,
            "environmental_impact": impact_report
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Make sure to allow running via uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
