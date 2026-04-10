# db.py
import sqlite3

DB_PATH = "voters.db"

def get_from_db(nid_list):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    found = []
    not_found = []

    for nid in nid_list:
        cursor.execute("SELECT * FROM voters WHERE nid = ?", (nid,))
        row = cursor.fetchone()

        if row:
            found.append({
                "range_list": row[5],
                "id": row[1],
                "file_type": row[6],
                "nid": row[2],
                "name": row[3],
                "gender": row[4],
                "dob": row[5],
                "province_id": row[7],
                "province_name": row[8],
                "commune_id": row[9],
                "commune_name": row[10],
                "election_office_id": row[11],
                "election_office_name": row[12],
                "registration_year": row[13],
                "source": "database"
            })
        else:
            not_found.append(nid)

    conn.close()
    return found, not_found


def insert_to_db(results):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for voter in results:
        if "error" in voter:
            continue

        cursor.execute("""
            INSERT OR REPLACE INTO voters (
                id_number, nid, full_name, gender, dob, range_list, file_type,
                province_id, province_name, commune_id, commune_name,
                election_office_id, election_office_name, registration_year
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            voter.get("id"),
            voter.get("nid"),
            voter.get("name"),
            voter.get("gender"),
            voter.get("dob"),
            voter.get("range_list"),
            voter.get("file_type"),
            voter.get("province_id"),
            voter.get("province_name"),
            voter.get("commune_id"),
            voter.get("commune_name"),
            voter.get("election_office_id"),
            voter.get("election_office_name"),
            voter.get("registration_year")
        ))

    conn.commit()
    conn.close()