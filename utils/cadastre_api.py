cd /workspaces/Zami
cat > utils/cadastre_api.py << 'EOF'
"""
IGN Cadastre API - Property boundaries and parcel info
No API key needed
"""

import requests

def get_parcel_info(lat: float, lon: float, distance: int = 50) -> dict:
    """
    Get cadastral parcel information at coordinates
    
    Returns:
        Parcel number, surface, commune
    """
    
    url = "https://apicarto.ign.fr/api/cadastre/parcel"
    params = {"lat": lat, "lon": lon, "distance": distance}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            features = data.get('features', [])
            
            if features:
                props = features[0].get('properties', {})
                return {
                    "success": True,
                    "parcel_number": props.get('id_parcelle', 'N/A'),
                    "surface": props.get('surface_parcelle', 0),
                    "commune": props.get('nom_commune', 'N/A'),
                    "source": "cadastre_api"
                }
        
        return {
            "success": False,
            "parcel_number": "N/A",
            "surface": 0,
            "source": "unavailable",
            "message": "Cadastre data not available"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "source": "error"
        }
EOF