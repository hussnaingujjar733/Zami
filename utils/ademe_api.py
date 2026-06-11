# utils/ademe_api_v2.py
import requests
import streamlit as st
from typing import Dict, Optional

ADEME_BASE_URL = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe03existant"

def get_dpe_by_address(address: str, api_key: Optional[str] = None) -> Dict:
    """
    Get REAL DPE data from ADEME API
    
    Args:
        address: Full address string (e.g., "39 Rue du Sergent Bobillot 93100 Montreuil")
        api_key: Optional API key for higher rate limits
    
    Returns:
        Dictionary with dpe_rating, consumption, surface, year, etc.
    """
    
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    params = {
        "q": address,
        "size": 1,
        "select": "etiquette_dpe,conso_5_usages_ef,surface_habitable_logement,annee_construction,code_postal_ban,nom_commune_ban"
    }
    
    url = f"{ADEME_BASE_URL}/lines"
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            if results and len(results) > 0:
                result = results[0]
                return {
                    "success": True,
                    "dpe": result.get('etiquette_dpe', 'E'),
                    "consumption": result.get('conso_5_usages_ef', 280),
                    "surface": result.get('surface_habitable_logement', 75),
                    "year": result.get('annee_construction', 1970),
                    "postcode": result.get('code_postal_ban', ''),
                    "city": result.get('nom_commune_ban', ''),
                    "source": "ADEME_API"
                }
            else:
                return {
                    "success": False,
                    "message": "No DPE data found for this address",
                    "source": "no_data"
                }
        else:
            return {
                "success": False,
                "message": f"API Error: {response.status_code}",
                "source": "api_error"
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "source": "exception"
        }


def get_dpe_by_postcode(postcode: str, api_key: Optional[str] = None) -> Dict:
    """
    Get aggregated DPE statistics for a postal code
    
    Useful for showing average DPE in an area
    """
    
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    params = {
        "q": postcode,
        "size": 100,
        "select": "etiquette_dpe,conso_5_usages_ef"
    }
    
    url = f"{ADEME_BASE_URL}/lines"
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            if results:
                # Calculate statistics
                dpe_counts = {}
                total_consumption = 0
                
                for result in results:
                    dpe = result.get('etiquette_dpe')
                    if dpe:
                        dpe_counts[dpe] = dpe_counts.get(dpe, 0) + 1
                    
                    consumption = result.get('conso_5_usages_ef')
                    if consumption:
                        total_consumption += consumption
                
                return {
                    "success": True,
                    "sample_size": len(results),
                    "dpe_distribution": dpe_counts,
                    "avg_consumption": total_consumption / len(results) if results else 0,
                    "source": "ADEME_API"
                }
        
        return {"success": False, "message": "No data for this postal code"}
        
    except Exception as e:
        return {"success": False, "message": str(e)}


def get_dpe_by_city(city: str, api_key: Optional[str] = None) -> Dict:
    """
    Get DPE statistics for an entire city
    """
    
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    params = {
        "q": city,
        "size": 500,
        "select": "etiquette_dpe,conso_5_usages_ef"
    }
    
    url = f"{ADEME_BASE_URL}/lines"
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            if results:
                # Calculate statistics
                dpe_counts = {'A':0, 'B':0, 'C':0, 'D':0, 'E':0, 'F':0, 'G':0}
                consumptions = []
                
                for result in results:
                    dpe = result.get('etiquette_dpe')
                    if dpe and dpe in dpe_counts:
                        dpe_counts[dpe] += 1
                    
                    consumption = result.get('conso_5_usages_ef')
                    if consumption:
                        consumptions.append(consumption)
                
                return {
                    "success": True,
                    "city": city,
                    "sample_size": len(results),
                    "dpe_distribution": dpe_counts,
                    "avg_consumption": sum(consumptions) / len(consumptions) if consumptions else 0,
                    "source": "ADEME_API"
                }
        
        return {"success": False, "message": "No data for this city"}
        
    except Exception as e:
        return {"success": False, "message": str(e)}


# Test the API
if __name__ == "__main__":
    print("Testing ADEME API v2...")
    
    # Test 1: Get DPE by address
    result = get_dpe_by_address("39 Rue du Sergent Bobillot 93100 Montreuil")
    print(f"Address lookup: {result.get('success')} - DPE: {result.get('dpe')}")
    
    # Test 2: Get DPE by postal code
    result = get_dpe_by_postcode("93100")
    print(f"Postcode lookup: {result.get('success')} - Sample size: {result.get('sample_size')}")
    
    # Test 3: Get DPE by city
    result = get_dpe_by_city("Montreuil")
    print(f"City lookup: {result.get('success')} - Sample size: {result.get('sample_size')}")