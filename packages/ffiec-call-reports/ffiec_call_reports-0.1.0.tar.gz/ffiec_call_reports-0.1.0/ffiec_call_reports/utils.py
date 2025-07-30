"""
Utility functions for FFIEC Call Reports.
"""

from html import unescape
from bs4 import BeautifulSoup
import pandas as pd
from typing import Dict

def parse_xbrl_to_dataframe(content: str, rssd_id: str) -> pd.DataFrame:
    """
    Parse XBRL content into a DataFrame.
    
    Args:
        content: The XBRL content to parse
        rssd_id: The RSSD ID of the institution
        
    Returns:
        DataFrame containing the parsed data
    """
    content = unescape(content)
    soup = BeautifulSoup(content, "xml")
    xbrl_tag = soup.find("xbrl")
    if not xbrl_tag:
        raise ValueError("No <xbrl> element found in the file!")
    
    records = []
    for tag in xbrl_tag.find_all():
        if tag.has_attr("decimals"):
            fact_id = tag.name.split(":")[-1]
            records.append({
                "rssd_id": rssd_id,
                "id": fact_id,
                "value": tag.get_text(strip=True),
                "decimal": tag["decimals"]
            })
    return pd.DataFrame(records)

def get_mapping_dict(mapping_file: str = "downloads/taxonomy/MDRM/MDRM_CSV.csv") -> Dict[str, str]:
    """
    Load and process the MDRM mapping file.
    
    Args:
        mapping_file: Path to the MDRM mapping CSV file
        
    Returns:
        Dictionary mapping metric IDs to their descriptions
    """
    mdrm_df = pd.read_csv(
        mapping_file,
        skiprows=1,
        dtype={"Mnemonic": str, "Item Code": str}
    )
    
    mdrm_df["metric"] = (
        mdrm_df["Mnemonic"].str.strip() +
        mdrm_df["Item Code"].str.zfill(4)
    )
    
    return pd.Series(
        mdrm_df["Item Name"].values,
        index=mdrm_df["metric"]
    ).to_dict()

def apply_mapping(df: pd.DataFrame, mapping_dict: Dict[str, str]) -> pd.DataFrame:
    """
    Apply metric mapping to a DataFrame.
    
    Args:
        df: DataFrame containing the call report data
        mapping_dict: Dictionary mapping metric IDs to descriptions
        
    Returns:
        DataFrame with added 'label' column
    """
    df = df.copy()
    df["label"] = df["id"].map(mapping_dict).fillna("Unknown metric")
    return df 