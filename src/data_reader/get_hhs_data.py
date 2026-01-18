"""
Using Socrata Open Data API (SODA)

This is the API used by healthdata.gov (and many other government open data portals). The query parameters like $where, $limit, $order are SODA query syntax (SoQL - Socrata Query Language).

"""

import requests
import pandas as pd
import json
from datetime import date

URL = "https://healthdata.gov/resource/g62h-syeh.json"
metadata_url = "https://healthdata.gov/api/views/g62h-syeh.json"

def retrieve_hhs_daily_data(state='CA'):
    # Get HHS daily admissions and hosputal capacity data for a state
    params = {
        "$where": f"state = '{state}' AND date >= '2020-10-16' AND date <= '{date.today()}'",
        "$limit": 50000,
        "$order": "date ASC",
    }
    
    r = requests.get(URL, params=params)
    data = r.json()

    return pd.DataFrame(data)


def get_hhs_metadata():
    # Get HHS Metadata, schema info from Socrata API
    r = requests.get(metadata_url)
    metadata = r.json()

    # Extract just the columns info
    columns = metadata.get("columns", [])
    return pd.DataFrame([
        {
            "name": c["fieldName"],
            "type": c["dataTypeName"],
            "description": c.get("description", "")
        }
        for c in columns
    ])