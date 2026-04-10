import requests
import json

API_URL = "http://127.0.0.1:8000/api/search-nid"

def main():
    nids = input("Enter NID(s), separated by commas: ").split(",")
    nids = [nid.strip() for nid in nids]

    response = requests.post(API_URL, json={"nids": nids})

    if response.status_code == 200:
        print("\nResult (JSON):")
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    else:
        print("Error:", response.status_code, response.text)

if __name__ == "__main__":
    main()
