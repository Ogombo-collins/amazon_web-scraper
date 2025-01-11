import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Set up Selenium WebDriver
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (no browser UI)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Function to scrape reviews from a single page
def scrape_reviews_from_page(driver, url):
    driver.get(url)
    time.sleep(2)  # Allow the page to load fully
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    reviews = []

    # Locate all review blocks
    review_blocks = soup.find_all('span', {'data-hook': 'review-body'})
    for block in review_blocks:
        review_text = block.get_text(strip=True)
        reviews.append(review_text)

    return reviews

# Main scraper function
def scrape_amazon_reviews(base_url, pages, output_csv):
    driver = get_driver()
    all_reviews = []

    try:
        for page in range(1, pages + 1):
            print(f"Scraping page {page}...")
            url = base_url.format(page=page)
            reviews = scrape_reviews_from_page(driver, url)
            all_reviews.extend(reviews)

        # Save reviews to a CSV file
        df = pd.DataFrame({'Reviews': all_reviews})
        df.to_csv(output_csv, index=False, encoding='utf-8')
        print(f"Scraping completed! Reviews saved to {output_csv}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

# Define variables
base_url = "https://www.amazon.com/Things-Fall-Apart-Chinua-Achebe/product-reviews/0385474547/ref=cm_cr_getr_d_paging_btm_prev_1?ie=UTF8&reviewerType=all_reviews&pageNumber={page}"
pages_to_scrape = 50
output_file = "Amazon_Reviews.csv"

# Run scraper
if __name__ == "__main__":
    scrape_amazon_reviews(base_url, pages_to_scrape, output_file)

