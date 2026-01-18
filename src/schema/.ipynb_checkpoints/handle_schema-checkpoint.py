import pandas as pd
import requests

METADATA_URL = "https://healthdata.gov/api/views/g62h-syeh.json"


def get_metadata(metadata_url: str = METADATA_URL) -> dict:
    """Fetch full metadata from API.
    
    Returns:
        dict: Full metadata including dataset info and columns.
    """
    r = requests.get(metadata_url)
    if r.status_code != 200:
        return {}
    return r.json()
    
def get_schema_types(metadata_url: str = METADATA_URL) -> dict:
    """Fetch column types from API schema.
    
    Returns:
        dict: Mapping of column names to pandas dtypes.
    """
    metadata = get_metadata(metadata_url)
    if not metadata:
        return {}
    
    schema_to_pandas = {
        "text": "string",
        "number": "Float64",  # nullable float
        "calendar_date": "datetime64[ns]",
    }
    return {
        col["fieldName"]: schema_to_pandas.get(col["dataTypeName"], "object")
        for col in metadata.get("columns", [])
    }

def apply_schema_types(df: pd.DataFrame) -> pd.DataFrame:
    """Apply schema types to DataFrame columns.
    
    Args:
        df: DataFrame with string columns.
    
    Returns:
        DataFrame with proper types applied.
    """
    schema_types = get_schema_types()
    for col in df.columns:
        if col not in schema_types:
            continue
        
        dtype = schema_types[col]
        try:
            if dtype == "datetime64[ns]":
                df[col] = pd.to_datetime(df[col], errors="coerce")
            elif dtype in ("Float64", "Int64"):
                df[col] = pd.to_numeric(df[col], errors="coerce").astype(dtype)
            elif dtype == "string":
                df[col] = df[col].astype("string")
        except Exception:
            pass  # Keep original type if conversion fails
    
    return df
