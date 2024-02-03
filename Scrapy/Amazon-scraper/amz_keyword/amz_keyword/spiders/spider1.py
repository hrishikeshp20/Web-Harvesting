import scrapy
from subprocess import call
import csv
import re


def open_csv_file():
    call(["python", "csv_concate.py"])


#open_csv_file()


class Spider1Spider(scrapy.Spider):
    name = "spider1"



    def start_requests(self):

        with open('input.csv', 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                # Extract the keyword and URL from the CSV
                keyword = row['Keyword']
                words = keyword.split()

                # Check if there are multiple words
                if len(words) > 1:
                    # Join the words with a '+', without any space
                    keyword = '+'.join(words)

                amazon_search_url = f'https://www.amazon.com/s?k={keyword}&page=1'
                row['Amazon_Search_URL'] = amazon_search_url
                yield scrapy.Request(amazon_search_url, callback=self.parse_keywords,
                                     meta={'keyword': keyword, 'row_data': row})




    def parse_keywords(self, response):
        keyword = response.meta['keyword']  # Extract the keyword
        row_data = response.meta['row_data']  # Extract the row data
        amazon_search_url = row_data.get('Amazon_Search_URL')

        title = response.xpath(
            '//div[@class="a-section a-spacing-small a-spacing-top-small"]//span[1]/text()').get()



        # Use a regular expression to extract the value between "over" and "results"
        match = re.search(r'(\S+)\s+results?', title)
        print("@@@@@@@@@@@@@@@@")
        print(match)
        print(title)

        if match:
            result_value = match.group(1).replace(',', '')  # Remove commas if present
            row_data['Product_count'] = result_value
        else:
            row_data['Product_count'] = title

        row_data['Product_url'] = amazon_search_url


        yield row_data
