from fastapi import FastAPI
from sec import SECReportFetcher
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import config

app = FastAPI()


@app.get("/")
def get_latest():
    return {'placeholder': 'This will be reserved for HTML page in future'}


@app.get("/{ticker}/{year}/{filing}")
def get_reports(year: str, ticker: str, filing: str):
    report = SECReportFetcher(filing, ticker)
    return {"file": report.get_filings(year)}


@app.get("/example")
def get_example_reports():
    year = str(datetime.now().year)
    
    AAPL = SECReportFetcher('10-K', 'AAPL')
    META = SECReportFetcher('10-K', 'META')
    GOOGL = SECReportFetcher('10-K', 'GOOGL')
    AMZN = SECReportFetcher('10-K', 'AMZN')
    NFLX = SECReportFetcher('10-K', 'NFLX')
    GS = SECReportFetcher('10-K', 'GS')
    
    return {
        'description': 'This is an example of retrieving the latest 10-K reports of 5 big companies.',
        'data': {
            "Apple": AAPL.get_filings(year),
            "Meta": META.get_filings(year),
            "Alphabet": GOOGL.get_filings(year),
            "Amazon": AMZN.get_filings(year),
            "Netflix": NFLX.get_filings(year),
            "Goldman Sachs": GS.get_filings(year)
            },
        }
    

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)