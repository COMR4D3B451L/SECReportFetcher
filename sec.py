import requests
import datetime
from fastapi import HTTPException
import config


class SECReportFetcher:
    def __init__(self, filing_type: str, ticker: str):
        self.filing_type = filing_type.upper()
        self.ticker = ticker.upper()
        self.headers = config.HEADERS
        self.cik = self.get_cik(self.ticker)
        self.cik_zeros = self.get_cik(self.ticker, zeros=True)
        self.url = config.SUBMISSIONS_URL + f'CIK{self.cik_zeros}.json'
        self.get_data()

    def get_cik(self, ticker: str, zeros: bool = False) -> str:
        """Retrieves the CIK number for a given ticker"""
        company_tickers_url = config.COMPANY_TICKERS_URL
        response = requests.get(company_tickers_url, headers=self.headers)
        response.raise_for_status()
        data = response.json()

        for item in data.values():
            if item["ticker"] == ticker:
                cik = item["cik_str"]
                if zeros:
                    zeros = "0" * (10 - len(str(cik)))
                    cik = zeros + str(cik)
                return str(cik)

        raise HTTPException(status_code=400, detail=f"Invalid ticker provided '{ticker}'.")

    def get_data(self):
        """Retrieves filing data from the SEC API"""
        response = requests.get(self.url, headers=self.headers)
        response.raise_for_status()
        data = response.json()

        self.forms = data["filings"]["recent"]["form"]
        self.accession_numbers = data["filings"]["recent"]["accessionNumber"]
        self.filing_dates = data["filings"]["recent"]["filingDate"]
        self.primary_documents = data["filings"]["recent"]["primaryDocument"]

    def get_filings_keys_for_year(self, year: str) -> list[int]:
        """Retrieves a list of filing keys for a given year"""
        keys_in_year = []
        for i, date_str in enumerate(self.filing_dates):
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            if str(date.year) == year:
                keys_in_year.append(i)
        return keys_in_year

    def build_url(self, key: int) -> str:
        """Builds the URL for a given filing key"""
        accession_number = self.accession_numbers[key].replace("-", "")
        primary_document = self.primary_documents[key]
        return config.EDGAR_URL + f"{self.cik}/{accession_number}/{primary_document}"

    def get_filings(self, _year: str) -> list[str]:
        """Retrieves a list of URLs for filings submitted in a given year"""
        urls = []
        year = self.validate_year(_year)
        keys = self.get_filings_keys_for_year(year)

        for key in keys:
            if self.forms[key] == self.filing_type:
                url = self.build_url(key)
                urls.append(url)
        if not urls:
            urls = self.handle_empty_list(year)
        return urls
    
    def handle_empty_list(self, year) -> list[str]:
        urls = self.get_filings(str(int(year) - 1))
        return urls

    def validate_year(self, year) -> str:
        current_year = datetime.datetime.now().year
        if int(year) > current_year:
            raise HTTPException(status_code=400, detail=f"The year specified '{year}' is in the future!")
        else:
            return str(year)