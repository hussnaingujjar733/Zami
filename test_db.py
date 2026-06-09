import data_store

print("--- STARTING DATABASE TEST ---")
dummy_lead = {
    "address": "123 Test Street",
    "zipcode": "75000",
    "dpe": "A",
    "surface": 100,
    "cost": 1000,
    "roi": 5.0,
    "name": "ZAMI Tester",
    "email": "test@thezami.com",
    "phone": "123456789"
}

try:
    print("Saving dummy lead...")
    data_store.create_new_lead(dummy_lead)
    print("--- TEST COMPLETE ---")
except Exception as e:
    print(f"ERROR: {e}")
