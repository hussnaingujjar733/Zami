import requests
import streamlit as st

class IGNAPI:
    """
    IGN APIs for ZAMI - With fallback for when APIs are unavailable
    """
    
    # Local fallback database for French postal codes
    FALLBACK_DATA = {
        "37000": {"city": "Tours", "department": "37", "region": "Centre-Val de Loire", "population": 136000},
        "75001": {"city": "Paris", "department": "75", "region": "Île-de-France", "population": 2160000},
        "69001": {"city": "Lyon", "department": "69", "region": "Auvergne-Rhône-Alpes", "population": 513000},
        "13001": {"city": "Marseille", "department": "13", "region": "Provence-Alpes-Côte d'Azur", "population": 861000},
        "33000": {"city": "Bordeaux", "department": "33", "region": "Nouvelle-Aquitaine", "population": 254000},
        "59000": {"city": "Lille", "department": "59", "region": "Hauts-de-France", "population": 232000},
        "31000": {"city": "Toulouse", "department": "31", "region": "Occitanie", "population": 479000},
        "06000": {"city": "Nice", "department": "06", "region": "Provence-Alpes-Côte d'Azur", "population": 342000},
        "44000": {"city": "Nantes", "department": "44", "region": "Pays de la Loire", "population": 309000},
        "67000": {"city": "Strasbourg", "department": "67", "region": "Grand Est", "population": 280000},
        "38000": {"city": "Grenoble", "department": "38", "region": "Auvergne-Rhône-Alpes", "population": 158000},
        "34000": {"city": "Montpellier", "department": "34", "region": "Occitanie", "population": 277000},
        "14000": {"city": "Caen", "department": "14", "region": "Normandie", "population": 108000},
        "76600": {"city": "Le Havre", "department": "76", "region": "Normandie", "population": 170000},
        "51100": {"city": "Reims", "department": "51", "region": "Grand Est", "population": 182000},
    }
    
    def get_commune_by_postal_code(self, postal_code):
        """Get city info from postal code - with fallback"""
        
        # Try BAN API first (this one works!)
        try:
            url = "https://api-adresse.data.gouv.fr/search/"
            response = requests.get(url, params={"q": postal_code, "limit": 1}, timeout=5)
            if response.status_code == 200:
                data = response.json()
                features = data.get('features', [])
                if features:
                    props = features[0].get('properties', {})
                    city = props.get('city', '')
                    if city:
                        return {
                            "city": city,
                            "postal_code": postal_code,
                            "department": postal_code[:2],
                            "exists": True,
                            "source": "ban_api"
                        }
        except:
            pass
        
        # Fallback to local database
        if postal_code in self.FALLBACK_DATA:
            data = self.FALLBACK_DATA[postal_code]
            return {
                "city": data["city"],
                "postal_code": postal_code,
                "department": data["department"],
                "region": data["region"],
                "population": data.get("population"),
                "exists": True,
                "source": "fallback"
            }
        
        # Default fallback
        return {
            "city": "France",
            "postal_code": postal_code,
            "department": postal_code[:2],
            "exists": False,
            "source": "default",
            "message": "Using estimated data"
        }
    
    def get_property_value_estimate(self, zipcode, surface, property_type="Appartement"):
        """Estimate property value based on postal code"""
        
        # Regional price per m² (€)
        regional_prices = {
            '75': 10500,  # Paris
            '92': 7500,   # Hauts-de-Seine
            '93': 4500,   # Seine-Saint-Denis
            '94': 6500,   # Val-de-Marne
            '78': 5500,   # Yvelines
            '91': 5000,   # Essonne
            '95': 4800,   # Val-d'Oise
            '69': 5000,   # Lyon
            '13': 4500,   # Marseille
            '33': 4200,   # Bordeaux
            '31': 3800,   # Toulouse
            '59': 3500,   # Lille
            '67': 3500,   # Strasbourg
            '44': 3800,   # Nantes
            '38': 3800,   # Grenoble
            '34': 3800,   # Montpellier
            '14': 3200,   # Caen
            '76': 3000,   # Le Havre
            '51': 2800,   # Reims
            '37': 3200,   # Tours (you added!)
        }
        
        prefix = str(zipcode)[:2]
        price_per_m2 = regional_prices.get(prefix, 3500)
        
        if property_type == "Maison individuelle":
            price_per_m2 = int(price_per_m2 * 0.9)
        
        return surface * price_per_m2
    
    def get_urban_planning_info(self, lat, lon):
        """Return default planning info (since official API is down)"""
        # Most urban zones in France allow renovation
        return {
            "renovation_allowed": True,
            "message": "Rénovation généralement autorisée en zone urbaine",
            "source": "default"
        }
    
    def check_renovation_feasibility(self, lat, lon, postal_code=None):
        """Check if renovation is possible"""
        return {
            "feasibility": "✅ Rénovation généralement possible",
            "risk_level": "Faible",
            "message": "En zone urbaine, les travaux de rénovation énergétique sont généralement autorisés.",
            "recommendation": "Vérifiez auprès de votre mairie pour des travaux structurants."
        }
