import os
import requests
from typing import Optional, Dict, Any

# Constants
CLIMATIQ_API_URL = "https://api.climatiq.io/data/v1/estimate"
# Using a common activity ID for electricity grid mix.
DEFAULT_ACTIVITY_ID = "electricity-supply_grid-source_residual_mix"

def get_carbon_emissions(energy_kwh: float, region: str = "US") -> Optional[Dict[str, Any]]:
    """
    Fetches carbon emission data from the Climatiq API based on energy usage.

    Args:
        energy_kwh (float): Energy consumption in kWh.
        region (str): The region code (e.g., 'US', 'GB', 'DE'). Defaults to 'US'.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing emission factor, unit,
                                 and carbon intensity, or None if the request fails.
    """
    api_key = os.getenv("CLIMATIQ_API_KEY")

    if not api_key:
        print("Warning: CLIMATIQ_API_KEY environment variable not set. Climatiq data unavailable.")
        return None

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Constructing the estimate request
    payload = {
        "emission_factor": {
            "activity_id": DEFAULT_ACTIVITY_ID,
            "region": region,
            "data_version": "^5" # Use recent data version
        },
        "parameters": {
            "energy": energy_kwh,
            "energy_unit": "kWh"
        }
    }

    try:
        response = requests.post(CLIMATIQ_API_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Extract relevant data
        co2e = data.get("co2e")
        co2e_unit = data.get("co2e_unit")
        
        # Calculate intensity if not directly provided
        carbon_intensity = 0.0
        if energy_kwh > 0 and co2e is not None:
            carbon_intensity = co2e / energy_kwh

        result = {
            "emission_factor": data.get("emission_factor", {}).get("activity_id", DEFAULT_ACTIVITY_ID),
            "unit": co2e_unit, 
            "carbon_intensity": round(carbon_intensity, 4),
            "total_emissions": co2e,
            "source": "Climatiq API"
        }
        
        return result

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Climatiq API: {e}")
        if e.response is not None:
             print(f"API Response: {e.response.text}")
        return None
    except Exception as e:
        print(f"Unexpected error in Climatiq API module: {e}")
        return None


