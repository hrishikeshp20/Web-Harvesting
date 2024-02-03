from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import csv


def school_scrape():
    # Initialize the Selenium WebDriver (you will need to have the appropriate driver installed)
    driver=webdriver.Chrome()

    driver.get('https://nurserylive.com/collections/plants')
    category_selector = driver.find_element(By.XPATH,'(//li[contains(@class,"indoor-plants")])[4]//a')
    category1 = category_selector.get_attribute('href')
    print(category1)

    element_url_selector = driver.find_element(By.XPATH,'(//li[contains(@class,"indoor-plants")])[4]//a')
    element_url = element_url_selector.get_attribute('href')
    driver.get(element_url)

    with open('plant_details.csv', 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write headers
        csv_writer.writerow(
            ["Name", "Short Description", "Description", "Regular Price", "Sale Price", "Categories", "Images"])



        element_to_scroll_to = driver.find_element(By.XPATH,'(//h2[@class="home-section--title"])[1]')

        #scroll_to_bottom_script = "window.scrollTo(0, document.body.scrollHeight);"
        #driver.execute_script(scroll_to_bottom_script)
        actions = ActionChains(driver)
        actions.move_to_element(element_to_scroll_to)
        actions.perform()

        counter = 3
        starter1 = 1
        while starter1 <= counter:
            product_counter1 = driver.find_elements(By.XPATH,'//div[@class="productgrid--wrapper"]//li[contains(@class,"productitem")]')
            product_counter1 = len(product_counter1)
            print(product_counter1)
            element_to_scroll_to = driver.find_element(By.XPATH, '(//h2[@class="home-section--title"])[1]')

            # scroll_to_bottom_script = "window.scrollTo(0, document.body.scrollHeight);"
            # driver.execute_script(scroll_to_bottom_script)
            actions = ActionChains(driver)
            actions.move_to_element(element_to_scroll_to)
            actions.perform()
            starter1 += 1
            print(f'starter= {starter1}')
            time.sleep(5)
            product_counter2 = driver.find_elements(By.XPATH,'//div[@class="productgrid--wrapper"]//li[contains(@class,"productitem")]')
            product_counter2 = len(product_counter2)
            print(product_counter2)
            print("====================================================")

            if product_counter1 == product_counter2:
                break
        products = driver.find_elements(By.XPATH, '//div[@class="productgrid--wrapper"]//li[contains(@class,"productitem")]')
        print(len(products))
        url_db = []
        for product in products:
            product_url_selector = product.find_element(By.XPATH,'(.//a[contains(@class,"productitem")])[1]')
            product_url = product_url_selector.get_attribute('href')
            url_db.append(product_url)

        print(f'length of db= {len(url_db)}')
        print(url_db)
        csv_data = []
        counter2 = 0
        for  url in url_db:
            counter2 += 1
            print(f"URL Index: {counter2}/{len(url_db)}, URL: {url}")
            print("---------------------------")
            driver.get(url)
            time.sleep(5)
            product_title_selector = driver.find_element(By.XPATH, '//h1[contains(@class,"product-title")]')
            product_title = product_title_selector.text
            name = product_title
            print(f'name- {product_title}')
            print("---------------------------")
            product_short_description_selector = driver.find_element(By.XPATH, '(//div[contains(@class,"product-short-description")])[1]')
            product_short_description_unclean = product_short_description_selector.get_attribute("outerHTML")
            product_short_description = re.sub(r'\n+', '\n', product_short_description_unclean)  # Replace multiple consecutive newlines with a single newline
            product_short_description = re.sub(r'\s{2,}', ' ', product_short_description)
            short_description = product_short_description
            print(f'short description- {product_short_description}')
            print("---------------------------")

            description_list = driver.find_elements(By.XPATH,'(//div[@class="description_section"])[1]//li')

            combined_string = ""
            for desc in description_list:
                description_selector = desc.find_element(By.XPATH,'.')
                description_unclean = description_selector.get_attribute("outerHTML")
                description_string = re.sub(r'\n+', '\n',description_unclean)  # Replace multiple consecutive newlines with a single newline
                description_string = re.sub(r'\s{2,}', ' ', description_string)
                combined_string += description_string
            print(f'description- {combined_string}')
            description = combined_string
            print("---------------------------")

            regular_price_selector = driver.find_element(By.XPATH, '(//div[@class="product-pricing"]//span[contains(@class,"single")])[1]')
            regular_price = regular_price_selector.text
            print(f'regular price- {regular_price}')
            print("---------------------------")

            sale_price_selector = driver.find_element(By.XPATH, '//div[@class="product-pricing"]//div[contains(@class,"sale")]//span[contains(@class,"money")]')
            sale_price = sale_price_selector.text
            print(f'sale price- {sale_price}')
            print("---------------------------")

            categories = "Indoor Plants"
            print(f'categories- {categories}')
            print("---------------------------")

            combined_img_string = ""
            image_list = driver.find_elements(By.XPATH, '//div[contains(@class,"product-gallery")]//img[not(contains(@src,"crop"))]')
            for img in image_list:
                image_selector = img.find_element(By.XPATH, '.')
                image = image_selector.get_attribute('src')

                combined_img_string += f'{image}, '
            print(f'image- {combined_img_string}')
            images = combined_img_string
            csv_writer.writerow([name, short_description, description, regular_price, sale_price, categories, images])
            csv_file.flush()


school_scrape()