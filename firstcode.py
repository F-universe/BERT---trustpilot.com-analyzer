from flask import Flask, request, render_template
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

# Path to the WebDriver
webdriver_path = "C:\\Users\\Fabio\\Desktop\\WEBDRIVER\\chromedriver-win64\\chromedriver.exe"

# Path to the output file
output_file_path = "C:\\Users\\Fabio\\Desktop\\BERT-(trustpilot.com) analyzer\\data.txt"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    company_name = request.form['company-name']
    base_url = f"https://it.trustpilot.com/review/{company_name}.com?languages=all&page="

    # Set up Selenium WebDriver
    service = Service(webdriver_path)
    driver = webdriver.Chrome(service=service)

    try:
        current_page = 1  # Start from the first page

        with open(output_file_path, "w", encoding="utf-8") as file:
            while True:
                url = base_url + str(current_page)
                driver.get(url)
                print(f"Navigating to {url}")

                try:
                    # Wait for the reviews container to load
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "styles_reviewsContainer__3_GQw"))
                    )
                    review_cards = driver.find_elements(By.CLASS_NAME, "styles_cardWrapper__LcCPA.styles_show__HUXRb.styles_reviewCard__9HxJJ")

                    if not review_cards:
                        print("No reviews found. End of pages.")
                        break

                    for card in review_cards:
                        try:
                            review_content = card.find_element(By.CLASS_NAME, "typography_body-l__KUYFJ.typography_appearance-default__AAY17.typography_color-black__5LYEn")
                            # Write the review content to the file in the required format
                            file.write(f'"{review_content.text}",\n\n')
                            print(f"Review saved: {review_content.text[:100]}...")
                        except NoSuchElementException:
                            print("No review content found in this card.")

                    current_page += 1  # Move to the next page

                except TimeoutException:
                    print("Timeout reached, ending scraping.")
                    break

    finally:
        driver.quit()

    return f"<h2>Scraping completed. Reviews saved to file.</h2><br><a href='/'>Go Back</a>"

if __name__ == "__main__":
    app.run(debug=True)
