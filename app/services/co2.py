import requests, logging, os, json
from django.utils import timezone
from app.models import Participation 

URL = "https://api.climatiq.io/data/v1/estimate"
MY_API_KEY = "A85887YKPS2P74AXK2NKS0MGSG"

HEADERS = {"Authorization" : f"Bearer {MY_API_KEY}"}

TIMEOUT  = 10      # secondes

def fetch_co2(weight_kg: float, activity_id: str, region: str = "FR") -> float:
    payload = {
        "emission_factor": {
            "activity_id": activity_id,
            "region": region,
        },
        "parameters": {
            "weight": weight_kg,
            "weight_unit": "t"
        }
    }
    print(payload)
    try:
        resp = requests.post(URL, json=payload, headers=HEADERS).json()
        print(resp)
        # return resp["co2e"]
    except requests.RequestException as exc:
        logging.error("Climatiq error: %s", exc)
        raise

def compute_and_save_impact(participation: Participation) -> None:

    unit = participation.challenge.unit

    if unit.name.lower() == "kg" or unit.nom.lower() == "kg":
        weight_total = participation.action_quantity  
        activity_id  = "waste_type_mixed-waste_method_recycled" 
    elif unit.weight_kg and unit.activity_id:
        weight_total = int(participation.action_quantity) * float(unit.weight_kg)
        activity_id  = unit.activity_id
    else:
        participation.impact_status = "ERROR"
        participation.save(update_fields=["impact_status"])
        return

    kg_co2 = fetch_co2(weight_total, activity_id)

    participation.impact_co2e          = kg_co2
    participation.impact_unit          = "kg"
    participation.impact_calculated_at = timezone.now()
    participation.impact_status        = "DONE"

    participation.save(update_fields=[
        "impact_co2e",
        "impact_unit",
        "impact_calculated_at",
        "impact_status"
    ])
