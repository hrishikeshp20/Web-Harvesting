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

driver = webdriver.Chrome()


def weather_parser():
    df = pd.DataFrame()
    years_loop, months_loop = year_month_gen()


    for year in years_loop:
        for month in months_loop:
            url = f'https://www.wunderground.com/history/monthly/in/pune/VAPO/date/{year}-{month}'
            driver.get(url)
            time.sleep(15)
            print(f'url- {url}')

            day_loop_selector = driver.find_elements(By.XPATH,'(//div[contains(@class,"observation-table")]//tbody/tr/td/table)[1]/tr[position() > 1]')
            counter3 = 1
            for day_loop in day_loop_selector:
                row_data_xpath = f'//div[contains(@class,"observation-table")]//tbody/tr/td/table/tr[position() > 1][{counter3}]//td'


                date_selector = driver.find_element(By.XPATH, (f'({row_data_xpath})' + '[1]'))
                date = date_selector.get_attribute("textContent")
                date = date.replace(" ", "")

                if len(str(date)) == 1:
                    date = f'0{date}'
                else:
                    pass

                if len(str(month)) == 1:
                    month = f'0{month}'
                else:
                    pass

                date1 = f'{date}-{month}-{year}'
                #df["Date"][counter3 - 1] = date1
                #df.loc[(counter3 - 1), "date"] = date1
                print(f'date1- {date1}')
                counter3 += 1

                column_dict = {'date': date1}

                column_names = ["max_temp", "avg_temp", "min_temp", "max_dew", "avg_dew", "min_dew",
                                "max_humidity", "avg_humidity",
                                "min_humidity", "max_wind_speed", "avg_wind_speed", "min_wind_speed", "max_pressure",
                                "avg_pressure", "min_pressure",
                                "precipitation"]

                column_dict.update({column: None for column in column_names})
                counter2 = 2
                counter4 = 0
                for column in column_names:
                    globals()[column] = driver.find_element(By.XPATH,
                                                            (f'({row_data_xpath})' + f'[{counter2}]')).get_attribute(
                        "textContent")
                    # date = date_selector.get_attribute("textContent")
                    column_dict[column] = globals()[column]


                    counter2 += 1

                    counter4 += 1

                new_row_df = pd.DataFrame([column_dict], columns = column_dict.keys())
                #result_df = df.concat(new_row_df, ignore_index=True)
                df = pd.concat([df, new_row_df], ignore_index=True)
                #print(df)

    return df








def year_month_gen():
    year_list = []
    for i in range(10, 24):
        year = f"{20}{i}"
        year_list.append(year)

    #month_list = range(1, 13)
    month_list = range(1, 13)


    return year_list, month_list


dataframe = weather_parser()
dataframe.to_csv('pune_weather_data.csv', index=False)



