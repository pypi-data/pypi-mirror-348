"""
Data models for FFIEC Call Reports.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import pandas as pd

@dataclass
class CallReport:
    """Represents a single call report."""
    
    rssd_id: int
    period_end_date: str
    data: pd.DataFrame
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert the call report to a DataFrame."""
        return self.data
    
    def to_csv(self, path: str) -> None:
        """Save the call report to a CSV file."""
        self.data.to_csv(path, index=False)
    
    def get_metric(self, metric_id: str) -> Optional[float]:
        """
        Get the value of a specific metric.
        
        Args:
            metric_id: The ID of the metric to retrieve
            
        Returns:
            The value of the metric if found, None otherwise
        """
        row = self.data[self.data['id'] == metric_id]
        if row.empty:
            return None
        return float(row.iloc[0]['value'])
    
    def get_metrics(self, metric_ids: list) -> dict:
        """
        Get multiple metrics at once.
        
        Args:
            metric_ids: List of metric IDs to retrieve
            
        Returns:
            Dictionary mapping metric IDs to their values
        """
        return {
            metric_id: self.get_metric(metric_id)
            for metric_id in metric_ids
        } 