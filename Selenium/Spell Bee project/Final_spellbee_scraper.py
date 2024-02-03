import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException


def spell_bee_scrape():

    exception_list = []

    global global_counter21

    options = webdriver.ChromeOptions()
    options.add_extension('MGIJMAJOCGFCBEBOACABFGOBMJGJCOJA_4_1_8_0.crx')
    driver = webdriver.Chrome(options=options)

    extension_popup = "chrome-extension://mgijmajocgfcbeboacabfgobmjgjcoja/browser_action.html"
    driver.get(extension_popup)

    input_field = driver.find_element(By.XPATH, '//input[@type="text"]')
    define_button = driver.find_element(By.XPATH, '//button[@id="define-btn"]')

    for i in range(global_counter21, global_loop_repeater1):

        print(f" Word = {words_db.loc[i,'Words']}")  # All print statement here are to show that the scraper
                                                     # is getting data as intended

        word_to_enter = words_db.loc[i, "Words"]     # Here Name is column name of Excel/csv file,
                                                     # change according to your column name

        user_input = word_to_enter
        user_input = user_input.lower()

        print(f"keyword= {user_input}")

        input_field.send_keys(user_input)
        define_button.click()
        time.sleep(5)

        try:
            word_break_selector = driver.find_element(By.XPATH, '//span[@class="headword"]')
        except Exception as e:
            print(f"Exception-{e}")
            time.sleep(5)
            pass

        try:
            word_break_selector = driver.find_element(By.XPATH, '//span[@class="headword"]')
        except Exception as e:
            print(f"Exception-{e}")
            pass

        # input_field.clear()

        word_break_selector = driver.find_element(By.XPATH, '//span[@class="headword"]')
        word_break_text = word_break_selector.text
        print(f"word break- {word_break_text}")

        phonetics = driver.find_elements(By.XPATH, '//div[@class="headword-box"]//span[@class="phonetics-text"]')
        phonetic_string = ""
        for phonetic in phonetics:
            phonetic_selector = phonetic.find_element(By.XPATH, '.')
            phonetic_text = phonetic_selector.text
            print(f"phonetics- {phonetic_text}")
            phonetic_string += phonetic_text + ","

        print(f"phonetic_string = {phonetic_string}")

        meaning_selector = driver.find_element(By.XPATH, '(//li[@class="sense"])[1]/child::div[1]')
        meaning_text = meaning_selector.text
        print(f"meaning- {meaning_text}")
        print("---------------------------------------------------------------------\n")
        input_field.clear()
        print(f"Outer- {(meaning_text and phonetic_string and word_break_text) == ''}")
        print(f"Outer- {exception_list}")

        if (meaning_text and phonetic_string and word_break_text) =="":
            print((meaning_text and phonetic_string and word_break_text) =="")
            #continue_program1()
            exception_list.append("2")
            pass

        if len(exception_list) > 0:
            print(exception_list)

            continue_program1()

        spell_bee_database.loc[global_counter21] = [user_input, word_break_text, phonetic_string, meaning_text]

        global_counter21 = i + 1
        print(f"^^^^{global_counter21}")

        print(spell_bee_database)
        print(f"global_counter21 == {global_counter21} compare global_loop_repeater1 =={global_loop_repeater1}")
        if global_counter21 >= global_loop_repeater1:
            return

    print("Code executed successfully")









def continue_program1():

    while True:
        user_input = input("Do you want to re run the program? (y/n): ")
        user_input = user_input.lower()
        check_list = ["y", "n"]
        if user_input not in check_list:
            print("Please enter only y or n")
        else:
            break

    if user_input == "y":

        exception_handler()
    else:
        pass


def exception_handler():
    # It will create the Excel file of data captured if the program is interrupted by network issues or
    # gets blocked by Google
    global global_counter21
    global global_loop_repeater1
    if global_counter21 >= global_loop_repeater1:
        return
    try:
        spell_bee_scrape()
    except Exception as e:

        print(f"An exception occurred: {e}")
        print("Data captured is incomplete because of failure")


        continue_program1()

        spell_bee_database.to_excel("scrapped_spell_bee_Data.xlsx", index=False)
        print("Program has ended")


words_db = pd.read_csv("spell_bee_input.csv") #Use ".read_excel" to read excel file
global_loop_repeater1 = len(words_db)

global_counter21 = 0

columns = ['Input', 'Word_break', 'Phonetics', 'meaning']
spell_bee_database = pd.DataFrame(columns=columns)  # all the scraped data will be stored here
exception_handler()
spell_bee_database.to_excel("scrapped_spell_bee_Data.xlsx", index=False)