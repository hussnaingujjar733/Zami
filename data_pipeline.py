import pandas as pd

def preprocess_features(surface, dpe, zipcode):
    """
    Raw inputs ko machine learning input vector format mein structured karta hai.
    """
    # DPE letter scores ko standard numerical scales mein map karne ke liye (Label Encoding baseline)
    dpe_mapping = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7}
    dpe_numeric = dpe_mapping.get(str(dpe).upper().strip(), 4) # Default to D if invalid
    
    # Zipcode text verification
    try:
        zip_clean = int(str(zipcode).strip()[:5])
    except ValueError:
        zip_clean = 75000 # Default fallback context
        
    features = {
        "surface_habitable": float(surface),
        "dpe_score": int(dpe_numeric),
        "postal_code": int(zip_clean)
    }
    
    # Dataframe return taake model directly vector matrix calculate kar sake
    return pd.DataFrame([features])