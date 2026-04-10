

CREATE TABLE voters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_number INTEGER,
    nid TEXT UNIQUE,
    full_name TEXT,
    gender TEXT,
    dob DATE,
    range_list INTEGER,
    file_type TEXT,
    province_id TEXT,
    province_name TEXT,
    commune_id TEXT,
    commune_name TEXT,
    election_office_id TEXT,
    election_office_name TEXT,
    registration_year TEXT
);
