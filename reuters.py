import requests
import json


url = 'https://selectapi.datascope.refinitiv.com/RestApi/v1'


def get_DSSToken():
    endpoint = '/Authentication/RequestToken'
    headers = {
        'Prefer': 'respond-async',
        'Content-Type': 'application/json'
    }
    body = {
        "Credentials": {
            "Username": "9020780",
            "Password": "BuzSup@1"
        }
    }
    r = requests.post(url = url+endpoint, headers=headers, data=json.dumps(body))
    return r.json()['value']



authToken = get_DSSToken()

endpoint = '/Extractions/ExtractWithNotes'

headers = {
    'Prefer': 'respond-async, wait=5',
    'Content-Type': 'application/json',
    'Authorization': 'Token ' + authToken
}


body = {
  "ExtractionRequest": {
    "@odata.type": "#DataScope.Select.Api.Extractions.ExtractionRequests.EndOfDayPricingExtractionRequest",
    "ContentFieldNames": [
      "Ask Price",
      "Asset Category",
      "Asset Category Description",
      "Asset ID",
      "Asset Status",
      "Asset Status Description",
      "Asset SubType",
      "Asset SubType Description",
      "Asset Type",
      "Asset Type Description",
      "Bid Price",
      "Block Trades",
      "CIN Code",
      "Common Code",
      "Currency Code",
      "Currency Code Description",
      "Currency Code Scaled",
      "Currency Code Scaled Description",
      "CUSIP",
      "Exchange Code",
      "Exchange Description",
      "Exercise Style",
      "Expiration Date",
      "File Code",
      "High Price",
      "Instrument ID",
      "Instrument ID Type",
      "ISIN",
      "Issuer OrgID",
      "Lot Size",
      "Low Price",
      "Market MIC",
      "MIC",
      "Mid Price",
      "Net Asset Value",
      "Number of Price Moves",
      "Offer Price",
      "Official Close Price",
      "Open Price",
      "Previous Close Price",
      "Put Call Indicator",
      "Quote ID",
      "RCP ID",
      "RIC",
      "Security Description",
      "SEDOL",
      "Settlement Date",
      "Settlement Price",
      "SICC",
      "Sicovam",
      "Strike Price",
      "Ticker",
      "Trade Date",
      "Trading Status",
      "Trading Symbol",
      "Turnover",
      "Underlying RIC",
      "Universal Ask Price",
      "Universal Bid Ask Date",
      "Universal Bid Price",
      "Universal Close Price",
      "Usage Instrument SubType",
      "Usage Instrument Type",
      "Valoren",
      "Volume",
      "VWAP Price",
      "Wertpapier"
    ],
    "IdentifierList": {
      "@odata.type": "#DataScope.Select.Api.Extractions.ExtractionRequests.InstrumentIdentifierList",
      "InstrumentIdentifiers": [
      { "Identifier": "438516AC0", "IdentifierType": "Cusip" },
      { "Identifier": "IBM.N", "IdentifierType": "Ric" }
      ]
    },
    "Condition": None
  }
}


r = requests.post(url = url+endpoint, headers=headers, data=json.dumps(body))

print(r.json())