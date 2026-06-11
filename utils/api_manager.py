cd /workspaces/Zami
cat > utils/api_manager.py << 'EOF'
"""
API Manager - Centralized API calls for ZAMI
"""

import streamlit as st
from utils.ademe_api import get_dpe_data
from utils.dvf_api import get_property_value
from utils.cadastre_api import get_parcel_info

class ZAMIManager:
    """Central API manager for ZAMI"""
    
    def __init__(self):
        self.api_sources = {
            "ademe": "ADEME (Official DPE Data)",
            "dvf": "DVF (Real Property Values)",
            "cadastre": "IGN (Property Boundaries)",
            "ban": "BAN (Address Search)"
        }
    
    def get_complete_property_info(self, address: str, lat: float, lon: float, 
                                   zipcode: str, surface: float) -> dict:
        """
        Fetch all property information from all APIs
        """
        
        result = {
            "address": address,
            "dpe_info": {},
            "value_info": {},
            "parcel_info": {},
            "success": True
        }
        
        # 1. Get DPE data (needs API key)
        with st.spinner("🔍 Fetching DPE data from ADEME..."):
            dpe = get_dpe_data(address)
            result["dpe_info"] = dpe
        
        # 2. Get property value
        with st.spinner("💰 Fetching property values from DVF..."):
            value = get_property_value(zipcode, surface)
            result["value_info"] = value
        
        # 3. Get cadastre info
        with st.spinner("🗺️ Fetching cadastre data..."):
            parcel = get_parcel_info(lat, lon)
            result["parcel_info"] = parcel
        
        # 4. Check if any API succeeded
        if (dpe.get('source') == 'fallback' and 
            value.get('source') != 'dvf_api' and 
            parcel.get('source') != 'cadastre_api'):
            st.warning("⚠️ Using estimated data. Real API data unavailable.")
        
        return result


# Singleton instance
_zami_manager = None

def get_zami_manager():
    global _zami_manager
    if _zami_manager is None:
        _zami_manager = ZAMIManager()
    return _zami_manager
EOF