from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import argparse
import pandas as pd


def parse_arguments():
    parser = argparse.ArgumentParser(description="Scrape comments from a webpage and save to CSV.")
    parser.add_argument("--url",
                        default="https://www.digikala.com/product/dkp-581373/%D9%BE%D9%86%DA%A9%D9%87-%D8%B1%D9%88%D9%85%DB%8C%D8%B2%DB%8C-%D8%AF%D9%85%D9%86%D8%AF%D9%87-%D9%85%D8%AF%D9%84-haleh/",
                        help="URL of the webpage to scrape")
    parser.add_argument("--output_dir", default='diji_comments_scraped.csv', help="Output CSV file path")
    return parser.parse_args()


def clicker(span):
    try:
        span.click()
    except:
        clicker(span)


class DigikalaCommentScraper:

    def __init__(self, URL):
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")  # This enables headless
        # Create a WebDriver instance (e.g., Chrome or Firefox)
        self.driver = webdriver.Firefox()  # You can use other drivers like Firefox or Edge
        # Navigate to the desired webpage

        self.driver.get(URL)
        time.sleep(5)
        # driver.execute_script("window.scrollTo(0, 200);")
        stopScrolling = 0
        # span = h1[0].find_elements(By.CLASS_NAME, "text-secondary-500")
        while True:
            stopScrolling += 1
            self.driver.execute_script("window.scrollBy(0,400)")
            time.sleep(0.05)

            self.h1 = self.driver.find_elements(By.CSS_SELECTOR, '#commentSection')

            span = self.h1[0].find_elements(By.CLASS_NAME, "text-secondary-500")

            if len(span) > 1 and ('دیدگاه دیگر' in span[0].text):
                print('button detected')
                clicker(span[0])
                break
            else:
                print('button has not detected')
        # return (self.h1, self.driver)

    def comment_scraper(self, start_page=1, number_of_pages=10):
        """
                Create a comments database by scraping comments from the webpage.

                Args:
                    start_page (int): The starting page number for scraping.
                    number_of_pages (int): The number of pages to scrape.

                Returns:
                    dict: A dictionary containing comments and labels of the Digikala product.
        """
        data = {'comments': [], 'labels': []}
        for page_number in range(number_of_pages):
            h2 = self.h1[0].find_elements(By.CSS_SELECTOR, "article")
            for e in h2:
                try:
                    h3 = e.find_element(By.CLASS_NAME, "text-body-2")
                    h4 = e.find_element(By.CLASS_NAME, "text-neutral-900")
                    data['comments'].append(h4.text)
                    data['labels'].append(h3.text)
                except:
                    pass

            spans = self.h1[0].find_elements(By.CLASS_NAME, "text-body2-strong")
            next_span = spans[-1]
            clicker(next_span)
            self.driver.execute_script("window.scrollBy(0,400)")
            time.sleep(0.1)
            self.driver.execute_script("window.scrollBy(0,400)")
            time.sleep(0.1)

            print(f"going to page {page_number + start_page}\n and number of data is {len(data['labels'])}")
        self.driver.quit()
        return data


def main():
    args = parse_arguments()
    scraper = DigikalaCommentScraper(args.url)

    comments1 = scraper.comment_scraper()
    db_comment1 = pd.DataFrame(comments1)
    db_comment1.to_csv(args.output_dir, encoding='utf-8-sig')


if __name__ == "__main__":
    main()
