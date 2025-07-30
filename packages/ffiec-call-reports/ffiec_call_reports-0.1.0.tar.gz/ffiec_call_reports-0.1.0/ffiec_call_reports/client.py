"""
FFIEC API Client for downloading Call Reports.
"""

import base64
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Optional, Union
import textwrap

from .models import CallReport
from .utils import parse_xbrl_to_dataframe

class FFIECClient:
    """Client for interacting with the FFIEC Call Reports API."""
    
    BASE_URL = "https://cdr.ffiec.gov/public/pws/webservices/retrievalservice.asmx"
    
    def __init__(self, username: str, passphrase: str):
        """
        Initialize the FFIEC client.
        
        Args:
            username: FFIEC API username
            passphrase: FFIEC API passphrase
        """
        self.username = username
        self.passphrase = passphrase
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
            "Content-Type": "application/soap+xml; charset=utf-8",
            "SOAPAction": "http://cdr.ffiec.gov/public/services/RetrieveFacsimile"
        }
    
    def _make_soap_body(self, rssd_id: int, period_end_date: str) -> str:
        """Build the SOAP envelope for the API request."""
        raw = f"""\
        <?xml version="1.0" encoding="utf-8"?>
        <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                         xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                         xmlns:soap12="http://www.w3.org/2003/05/soap-envelope"
                         xmlns:wsa="http://www.w3.org/2005/08/addressing">
          <soap12:Header>
            <wsa:Action>http://cdr.ffiec.gov/public/services/RetrieveFacsimile</wsa:Action>
            <wsa:To>https://cdr.ffiec.gov/public/pws/webservices/retrievalservice.asmx</wsa:To>
            <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
              <wsse:UsernameToken>
                <wsse:Username>{self.username}</wsse:Username>
                <wsse:Password>{self.passphrase}</wsse:Password>
              </wsse:UsernameToken>
            </wsse:Security>
          </soap12:Header>
          <soap12:Body>
            <RetrieveFacsimile xmlns="http://cdr.ffiec.gov/public/services">
              <dataSeries>Call</dataSeries>
              <reportingPeriodEndDate>{period_end_date}</reportingPeriodEndDate>
              <fiIDType>ID_RSSD</fiIDType>
              <fiID>{rssd_id}</fiID>
              <facsimileFormat>XBRL</facsimileFormat>
            </RetrieveFacsimile>
          </soap12:Body>
        </soap12:Envelope>"""
        return textwrap.dedent(raw).strip()
    
    def _fetch_facsimile(self, body: str) -> requests.Response:
        """Make the API request to fetch the call report."""
        response = requests.post(self.BASE_URL, data=body, headers=self.headers)
        response.raise_for_status()
        return response
    
    def _parse_response(self, response: requests.Response) -> Optional[str]:
        """Parse the API response and extract the XBRL content."""
        namespaces = {
            "soap": "http://schemas.xmlsoap.org/soap/envelope/",
            "ns": "http://cdr.ffiec.gov/public/services"
        }
        root = ET.fromstring(response.text)
        result = root.find(".//ns:RetrieveFacsimileResult", namespaces)
        
        if result is None or not result.text:
            return None
            
        return base64.b64decode(result.text).decode('utf-8')
    
    def get_call_report(
        self,
        rssd_id: Union[int, str],
        period_end_date: Union[str, datetime]
    ) -> Optional[CallReport]:
        """
        Download a call report for a specific RSSD ID and period.
        
        Args:
            rssd_id: The RSSD ID of the institution
            period_end_date: The end date of the reporting period (YYYY/MM/DD)
            
        Returns:
            CallReport object if successful, None if no data found
        """
        # Convert inputs to proper format
        rssd_id = int(rssd_id)
        if isinstance(period_end_date, datetime):
            period_end_date = period_end_date.strftime("%Y/%m/%d")
        
        # Make API request
        soap_body = self._make_soap_body(rssd_id, period_end_date)
        response = self._fetch_facsimile(soap_body)
        
        # Parse response
        xbrl_content = self._parse_response(response)
        if xbrl_content is None:
            return None
        
        # Parse XBRL to DataFrame
        df = parse_xbrl_to_dataframe(xbrl_content, str(rssd_id))
        
        return CallReport(
            rssd_id=rssd_id,
            period_end_date=period_end_date,
            data=df
        )
    
    def get_multiple_call_reports(
        self,
        rssd_ids: List[Union[int, str]],
        period_end_date: Union[str, datetime]
    ) -> List[CallReport]:
        """
        Download call reports for multiple RSSD IDs.
        
        Args:
            rssd_ids: List of RSSD IDs
            period_end_date: The end date of the reporting period (YYYY/MM/DD)
            
        Returns:
            List of CallReport objects (may be empty if no data found)
        """
        reports = []
        for rssd_id in rssd_ids:
            try:
                report = self.get_call_report(rssd_id, period_end_date)
                if report is not None:
                    reports.append(report)
            except Exception as e:
                print(f"Error processing RSSD ID {rssd_id}: {str(e)}")
                continue
        
        return reports 