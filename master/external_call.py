import requests
from django.conf import settings


def get_cities():
    """
    Get all cities from Raja Onkir Api
    """
    api_key = settings.RAJA_ONGKIR_API_KEY
    api_url = settings.RAJA_ONGKIR_API_URL
    response = requests.get(f"{api_url}/city", headers={"key": api_key})
    if response.status_code != 200:
        return []
    res_json = response.json()
    return res_json.get("rajaongkir", {}).get("results")
