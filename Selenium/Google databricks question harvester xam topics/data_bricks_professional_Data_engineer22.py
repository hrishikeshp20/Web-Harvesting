from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import requests
import time
import pandas as pd
import csv

driver = webdriver.Chrome()


def csv_loader():
    with open('databrick_questions.txt', 'w', encoding='utf-8') as file:
        file.write("DATABRICKS EXAM TOPIC QUESTION DUMP\n")
        file.write("\n")
        file.write("\n")
        file.write("\n")
        df = pd.read_csv('question_list_databrick.csv')
        for index, row in df.iterrows():
            link = row['url']
            driver.get(link)
            #time.sleep(5)
            question_scrape(file, link)
    driver.quit()


def question_scrape(file, link):
    time.sleep(5)
    question_box = driver.find_elements(By.XPATH, '//div[contains(@class,"discussion-header-container")]')

    for row in question_box:

        serial_selector = row.find_element(By.XPATH,
                                           './/div[contains(@class,"question-discussion-header")]/div[contains(.,"Quest")]')
        serial_num = serial_selector.text
        file.write(f"{serial_num}\n")
        file.write(f"Question link: {link}\n")
        file.write("--------------------------------------------------------------\n")
        print(serial_num)

        question_selector = row.find_element(By.XPATH, './/p[contains(@class,"card-text")]')
        question = question_selector.text
        question = re.sub(r'\n+', '\n', question).strip()
        file.write(f"{question}\n")
        file.write("--------------------------------------------------------------\n")
        print(question)

        try:
            option_selectors = row.find_elements(By.XPATH, './/li[contains(@class,"multi-choice-item")]')

            for option_selector in option_selectors:
                option = option_selector.get_attribute("textContent")
                option = re.sub(r'\s+', ' ', option).strip()
                option = option.replace("Most Voted", "***Most Voted***")
                file.write(f"{option}\n")

        except:
            file.write("XPATH NOT FOUND\n")

        file.write("--------------------------------------------------------------\n")

        correct_answer_selector = row.find_element(By.XPATH,
                                                   './/span[@class="correct-answer-box"]//span[@class="correct-answer"]')
        correct_answer = correct_answer_selector.get_attribute("textContent")

        if correct_answer == '':
            correct_answer_selector = row.find_element(By.XPATH,
                                                       './/span[@class="correct-answer-box"]//span[@class="correct-answer"]//img')
            correct_answer = correct_answer_selector.get_attribute('src')
            file.write(f"CORRECT ANSWER==: {correct_answer}\n")
        else:
            correct_answer = correct_answer_selector.get_attribute("textContent")
            file.write(f"CORRECT ANSWER==: {correct_answer}\n")

        file.write("###################################################################\n\n")


csv_loader()
