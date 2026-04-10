import json
from db import get_from_db, insert_to_db
from main import run_selenium

if __name__ == "__main__":
    nids_input = input("Enter NID(s), separated by commas: ").strip()
    nids = [nid.strip() for nid in nids_input.split(",") if nid.strip()]

    db_results, missing_nids = get_from_db(nids)

    selenium_results = run_selenium(missing_nids) if missing_nids else []
    insert_to_db(selenium_results)

    final_results = db_results + selenium_results

    output = {
        "count": len(final_results),
        "data": final_results,
        "status": "success" if final_results else "fail"
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))