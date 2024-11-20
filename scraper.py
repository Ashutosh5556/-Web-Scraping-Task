import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://www.yellowpages.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
SEARCH_TERM = "Digital Marketing Agencies"  
LOCATION = "California" 
PAGES_TO_SCRAPE = 3  
OUTPUT_FILE = "company_data.csv"  

def scrape_yellow_pages(search_term, location, pages_to_scrape):
    all_companies = []

    for page in range(1, pages_to_scrape + 1):
        print(f"Scraping page {page}...")
        search_url = f"{BASE_URL}search?search_terms={search_term.replace(' ', '%20')}&geo_location_terms={location.replace(' ', '%20')}&page={page}"
        response = requests.get(search_url, headers=HEADERS)

    
        if response.status_code != 200:
            print(f"Failed to fetch page {page}. HTTP Status Code: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        listings = soup.find_all("div", class_="result")  

        for listing in listings:
            try:
                
                name = listing.find("a", class_="business-name").text.strip() if listing.find("a", class_="business-name") else "N/A"
                website = listing.find("a", class_="track-visit-website")["href"] if listing.find("a", class_="track-visit-website") else "N/A"
                phone = listing.find("div", class_="phones phone primary").text.strip() if listing.find("div", class_="phones phone primary") else "N/A"
                address = listing.find("div", class_="street-address").text.strip() if listing.find("div", class_="street-address") else "N/A"
                category = search_term
                description = listing.find("div", class_="snippet").text.strip() if listing.find("div", class_="snippet") else "N/A"
                email = "N/A"  

                
                all_companies.append({
                    "Name": name,
                    "Website URL": website,
                    "Contact Number": phone,
                    "Location/Address": address,
                    "Industry/Category": category,
                    "Company Description": description,
                    "Email Address": email
                })
            except Exception as e:
                print(f"Error processing listing: {e}")

        
        time.sleep(2)

    return all_companies


def main():
    # Scrape data
    companies = scrape_yellow_pages(SEARCH_TERM, LOCATION, PAGES_TO_SCRAPE)

    # Save data to CSV
    if companies:
        df = pd.DataFrame(companies)
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"Data saved to {OUTPUT_FILE}")
    else:
        print("No data was scraped.")


if __name__ == "__main__":
    main()
