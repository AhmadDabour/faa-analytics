import requests
import os
from dotenv import load_dotenv
load_dotenv()
NOAA_API_KEY = os.getenv("NOAA_API_KEY")
headers = {"token": NOAA_API_KEY}
result = requests.get("https://www.ncei.noaa.gov/cdo-web/api/v2/stations?datasetid=GHCND&extent=40.54,-73.88,40.74,-73.68&limit=5&sortfield=datacoverage&sortorder=desc", headers=headers)
print(result.status_code)
print(result.text)