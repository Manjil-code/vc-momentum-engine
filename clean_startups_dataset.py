import pandas as pd
import re

INPUT_FILE = "data_sources/global_startups_500.csv"
OUTPUT_FILE = "data_sources/cleaned_global_startups.csv"

def generate_domain(name):
    if pd.isna(name):
        return None

    name = str(name).lower()
    name = re.sub(r'[^a-z0-9]', '', name)

    return f"https://{name}.com"

def normalize_sector(sector):
    if pd.isna(sector):
        return "Unknown"

    sector = str(sector).strip().lower()

    sector_map = {
        "fintech": "Fintech",
        "artificial intelligence": "AI",
        "healthcare": "HealthTech",
        "software": "SaaS",
        "e-commerce": "Ecommerce",
        "internet software & services": "SaaS"
    }

    return sector_map.get(sector, sector.title())

def normalize_region(country):
    if pd.isna(country):
        return "Unknown"

    country = str(country).strip()

    region_map = {
        "United States": "US",
        "USA": "US",
        "United Kingdom": "UK"
    }

    return region_map.get(country, country)

def clean_dataset():
    df = pd.read_csv(INPUT_FILE)

    cleaned = pd.DataFrame()

    cleaned["name"] = df["Company"]
    cleaned["website"] = df["Company"].apply(generate_domain)
    cleaned["sector"] = df["Industry"].apply(normalize_sector)
    cleaned["region"] = df["Country"].apply(normalize_region)

    cleaned = cleaned.dropna(subset=["name"])
    cleaned = cleaned.drop_duplicates(subset=["name"])

    cleaned = cleaned.head(600)

    cleaned.to_csv(OUTPUT_FILE, index=False)

    print(f"Cleaned dataset saved. Total companies: {len(cleaned)}")

if __name__ == "__main__":
    clean_dataset()
