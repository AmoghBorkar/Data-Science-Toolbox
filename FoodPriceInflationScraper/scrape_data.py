# Get the food prices data from WFP humdata website
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import math
from datetime import datetime

# Read in the list of URLs
countries = pd.read_csv(
    "https://data.humdata.org/dataset/31579af5-3895-4002-9ee3-c50857480785/resource/0f2ef8c4-353f-4af1-af97-9e48562ad5b1/download/wfp_countries_global.csv"
)
# Skip 1st row
countries = countries[1:]

all_countries_food_data = pd.DataFrame()

for index, row in countries.iterrows():
    url = row["url"]
    countryiso = row["countryiso3"]
    country = url.split("-")[-1].title()
    print(f"Reading data for {countryiso} from url: {url}")
    html_page = urlopen(url)
    soup = BeautifulSoup(html_page)
    csv_links = [x.get("href") for x in soup.findAll("a")]
    # Remove NaNs
    csv_links = [x for x in csv_links if x is not None]
    csv_links = [x for x in csv_links if ".csv" in x]
    country_csv_url = csv_links[0]
    country_data = pd.read_csv(f"https://data.humdata.org/{country_csv_url}")
    # Skip first row
    country_data = country_data[1:]
    country_data["country"] = country
    country_data["countryiso"] = countryiso
    country_data["url"] = url
    all_countries_food_data = all_countries_food_data.append(country_data)

    all_countries_food_data.astype("str").to_parquet(
        f"all_countries_food_price_data_{str(datetime.today().date()).replace('-','')}.parquet"
    )

