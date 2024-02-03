from selenium import webdriver
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def school_scrape():
    # Initialize the Selenium WebDriver (you will need to have the appropriate driver installed)
    driver=webdriver.Chrome()

    driver.get('https://nces.ed.gov/ccd/schoolsearch/')

    # Find the school name input field and type 'A' into it
    school_name = driver.find_element(By.XPATH, '//input[@name="InstName"]')
    time.sleep(10)
    school_name.send_keys('A')

    # Find and click the search button
    search_button = driver.find_element(By.XPATH, '(//input[contains(@value,"Search")])[2]')
    search_button.click()

    # Define custom headers
    custom_headers = ["Serial Number", "School Link", "School Name", "School Address", "Phone Number", "County", "Students", "Grade"]

    # Open a CSV file for writing
    with open('output1.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write the custom header row to the CSV file
        csv_writer.writerow(custom_headers)

        while True:
            try:
                # Wait for the "Next" button to be clickable
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//a[contains(.,"Next")]'))
                )
                # Find all school rows
                school_rows = driver.find_elements(By.XPATH, '//tbody//td//a[contains(@href,"school_detail")]/ancestor::tr[1]')

                for row in school_rows:
                    serial_num_selector = row.find_element(By.XPATH, './/td[1]')
                    serial_num = serial_num_selector.text

                    school_link_selector = row.find_element(By.XPATH, './/a')
                    school_link = school_link_selector.get_attribute('href')
                    if "https://nces.ed.gov/ccd/schoolsearch/" not in school_link:
                        school_link = "https://nces.ed.gov/ccd/schoolsearch/" + school_link
                    else:
                        pass

                    school_name_selector = row.find_element(By.XPATH, './/a//strong')
                    school_name = school_name_selector.text

                    school_address_selector = row.find_element(By.XPATH, './/a/ancestor::font[1]//font')
                    school_address = school_address_selector.text
                    school_address = school_address.replace('\xa0', ' ').strip()

                    phone_number_selector = row.find_element(By.XPATH, './/td[3]')
                    phone_number = phone_number_selector.text

                    county_selector = row.find_element(By.XPATH, './/td[4]')
                    county = county_selector.text

                    students_selector = row.find_element(By.XPATH, './/td[5]')
                    students = students_selector.text

                    grade_selector = row.find_element(By.XPATH, './/td[6]')
                    grade = grade_selector.text

                    # Write the row data to the CSV file
                    csv_writer.writerow([serial_num, school_link, school_name, school_address, phone_number, county, students, grade])

                # Click the "Next" button to navigate to the next page
                next_button.click()

            except Exception as e:
                # If an exception occurs or the "Next" button is not found, break the loop
                print("An error occurred:", str(e))
                break

    driver.quit()

# Run the scraping and CSV writing function
school_scrape()
