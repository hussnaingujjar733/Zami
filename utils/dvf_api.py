cd /workspaces/Zami
cat > utils/dvf_api.py << 'EOF'
"""
DVF API - Real property values from French government
No API key needed - Free and open
"""

import requests
from typing import Dict, Optional

def get_property_value(zipcode: str, surface: float, property_type: str = "Appartement") -> Dict:
    """
    Get real property value from DVF (Demandes de Valeurs Foncières)
    
    Args:
        zipcode: Postal code (e.g., "37000")
        surface: Property surface in m²
        property_type: "Appartement" or "Maison"
    
    Returns:
        Dictionary with estimated value and price per m²
    """
    
    url = "https://apicarto.ign.fr/api/dvf/communes"
    params = {
        "code_postal": zipcode,
        "surface_min": surface * 0.7,
        "surface_max": surface * 1.3,
        "type_local": property_type
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            prices_per_m2 = []
            
            for feature in data.get('features', []):
                props = feature.get('properties', {})
                price = props.get('valeur_fonciere')
                surf = props.get('surface_reelle_bati')
                
                if price and surf and surf > 0:
                    prices_per_m2.append(price / surf)
            
            if prices_per_m2:
                avg_price = sum(prices_per_m2) / len(prices_per_m2)
                return {
                    "success": True,
                    "value": int(surface * avg_price),
                    "price_per_m2": int(avg_price),
                    "source": "dvf_api",
                    "sample_size": len(prices_per_m2)
                }
        
        # Fallback to regional average
        return get_regional_fallback(zipcode, surface, property_type)
        
    except Exception as e:
        return {
            "success": False,
            "value": get_regional_fallback(zipcode, surface, property_type)['value'],
            "source": "fallback",
            "error": str(e)
        }


def get_regional_fallback(zipcode: str, surface: float, property_type: str) -> Dict:
    """Regional average prices when API fails"""
    
    regional_prices = {
        '75': 10500, '92': 7500, '93': 4500, '94': 6500,
        '78': 5500, '91': 5000, '95': 4800, '69': 5000,
        '13': 4500, '33': 4200, '31': 3800, '59': 3500,
        '67': 3500, '44': 3800, '38': 3800, '34': 3800,
        '37': 3200, '14': 3200, '76': 3000, '51': 2800
    }
    
    prefix = str(zipcode)[:2]
    price_per_m2 = regional_prices.get(prefix, 3500)
    
    if property_type == "Maison":
        price_per_m2 = int(price_per_m2 * 0.9)
    
    return {
        "success": True,
        "value": int(surface * price_per_m2),
        "price_per_m2": price_per_m2,
        "source": "regional_fallback"
    }
EOF