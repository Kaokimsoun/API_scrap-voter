# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from db import get_from_db, insert_to_db

app = FastAPI(title="Voter NID API")


class NIDRequest(BaseModel):
    nids: List[str]


def run_selenium(nid_list: List[str]):
    options = Options()
    # options.add_argument("--headless=new")  # enable if needed
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1200, 800)
    wait = WebDriverWait(driver, 15)

    results_data = []

    try:
        driver.get("https://voterlist.nec.gov.kh")

        for nid in nid_list:
            try:
                # Reset tab each time to prevent stale elements
                wait.until(EC.element_to_be_clickable((By.ID, "by_id")))
                nid_tab = driver.find_element(By.ID, "by_id")
                driver.execute_script("arguments[0].click();", nid_tab)

                # Find input field
                wait.until(EC.presence_of_element_located((By.ID, "id_no")))
                nid_input = driver.find_element(By.ID, "id_no")
                nid_input.clear()
                nid_input.send_keys(str(nid))

                # Click search
                wait.until(EC.element_to_be_clickable((By.ID, "btnSearchId")))
                search_btn = driver.find_element(By.ID, "btnSearchId")
                driver.execute_script("arguments[0].click();", search_btn)

                # Wait for table results
                wait.until(EC.presence_of_element_located((By.XPATH, "//table/tbody")))
                time.sleep(1)

                # Re-fetch rows after page update
                rows = driver.find_elements(By.XPATH, "//table/tbody/tr[position()>1]")
                found_any = False

                for row in rows:
                    cols = row.find_elements(By.TAG_NAME, "td")
                    data = [c.text.strip() for c in cols]

                    if len(data) > 5:
                        found_any = True
                        results_data.append({
                            "range_list": data[0],
                            "id": data[1],
                            "file_type": data[2],
                            "nid": str(nid),
                            "name": data[4],
                            "gender": data[5],
                            "dob": data[6],
                            "province_id": data[7].split(") ")[0].replace("(", ""),
                            "province_name": data[7].split(") ")[1] if ") " in data[7] else "",
                            "commune_id": data[8].split(") ")[0].replace("(", ""),
                            "commune_name": data[8].split(") ")[1] if ") " in data[8] else "",
                            "election_office_id": data[9].split(") ")[0].replace("(", ""),
                            "election_office_name": data[9].split(") ")[1] if ") " in data[9] else "",
                            "registration_year": data[10],
                            "source": "selenium"
                        })

                if not found_any:
                    results_data.append({
                        "nid": str(nid),
                        "error": "Not found on website"
                    })

            except Exception as e:
                results_data.append({
                    "nid": str(nid),
                    "error": str(e)
                })

    finally:
        driver.quit()

    return results_data


@app.get("/")
def home():
    return {"message": "✅ Voter NID API is running", "endpoint": "/api/search-nid"}


@app.post("/api/search-nid")
def search_multiple(request: NIDRequest):
    if not request.nids:
        raise HTTPException(status_code=400, detail="Missing NIDs")

    db_results, missing_nids = get_from_db(request.nids)
    selenium_results = run_selenium(missing_nids) if missing_nids else []
    insert_to_db(selenium_results)

    results = db_results + selenium_results
    return {"count": len(results), "data": results, "status": "success" if results else "fail"}


@app.post("/search")
def search_single(body: dict):
    nid = body.get("nid")
    if not nid:
        raise HTTPException(status_code=400, detail="Missing 'nid'")

    db_results, missing_nids = get_from_db([nid])
    selenium_results = run_selenium(missing_nids) if missing_nids else []
    insert_to_db(selenium_results)

    final_results = db_results + selenium_results
    return {
        "count": len(final_results),
        "data": final_results,
        "status": "success" if final_results and "error" not in final_results[0] else "fail"
    }