import requests
import csv
from bs4 import BeautifulSoup

# URL for UFC rankings
URL = "https://www.ufc.com/rankings"

def fetch_rankings(url):
    """Fetches and parses UFC rankings data."""
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    ranking_data = []

    ranking_sections = soup.find_all('div', class_='view-grouping')

    for section in ranking_sections:
        weight_class_header = section.find('div', class_='view-grouping-header')

        if weight_class_header:
            weight_class = weight_class_header.text.strip()
            champion_name_tag = section.find('h5').find('a')

            champion_name = champion_name_tag.text.strip() if champion_name_tag else "N/A"

            # Store champion information
            ranking_data.append([weight_class, "Champion", champion_name])

            # Get all ranked fighters
            fighters = section.find_all('td', class_='views-field-title')

            for rank, fighter in enumerate(fighters, start=1):
                fighter_name = fighter.find('a').text.strip()
                ranking_data.append([weight_class, rank, fighter_name])

    return ranking_data

def save_to_csv(data, filename="ufc_rankings.csv"):
    """Saves the scraped data to a CSV file."""
    if not data:
        print("No data to save.")
        return

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Weight Class", "Rank", "Fighter Name"])
        writer.writerows(data)

    print(f"Data saved successfully to {filename}")

if __name__ == "__main__":
    rankings = fetch_rankings(URL)
    save_to_csv(rankings)
