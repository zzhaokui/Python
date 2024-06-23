import time
import re
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ChromeDriver executable path (update with your actual path)
chrome_driver_path = 'C:/Program Files/Google/chromedriver.exe'

# Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless Chrome for faster execution

# Create a new Chrome session
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Base URL for scraping
base_url = 'https://www.trademe.co.nz/a/motors/cars/toyota/rav4/search?year_min=2018&odometer_max=80000&page={}'
# base_url = 'https://www.trademe.co.nz/a/motors/cars/honda/cr-v/search?year_min=2018&odometer_max=80000&page={}'

# Store scraped data
rav4_list = []


# Function to extract car data from the page
def extract_car_data(page_number):
    car_elements = driver.find_elements(By.CSS_SELECTOR, '.o-card')
    num_cars = len(car_elements)

    if num_cars == 1:
        print(f"Found 1 car on page {page_number}. Assuming no more new cars.")
        return False

    print(f"Found {num_cars} cars on page {page_number}")

    for car_element in car_elements:
        car_info = {}

        car_text = car_element.text
        lines = car_text.split('\n')

        try:
            title_element = car_element.find_element(By.CSS_SELECTOR, '.tm-motors-search-card__title')
            car_info['title'] = title_element.text.strip()
        except:
            car_info['title'] = 'N/A'

        # 将每一行信息存储到car_info中
        car_info['location'] = 'NA'
        for line in lines:
            year_match = re.search(r'\b\d{4}\b', line)  # 匹配四位数字，即年份
            # 使用简单的逻辑来判断信息类型并存储
            # if 'Toyota' in line or 'GX' in line or 'RAV4' in line:
            #     car_info['title'] = line
            if 'Asking price' in line:
                car_info['price'] = line.split('Asking price ')[-1]
            elif 'km' in line:
                car_info['odometer'] = line
            elif year_match:
                car_info['year'] = year_match.group()
            elif 'Auckland' in line or 'Wellington' in line or 'Christchurch' in line:
                car_info['location'] = line
            else:
                pass


        try:
            link_element = car_element.find_element(By.TAG_NAME, 'a')
            car_info['link'] = link_element.get_attribute('href')
        except:
            car_info['link'] = 'N/A'

        # Ensure 'title' and 'link' are not 'N/A' before adding to list
        if car_info.get('title') != 'N/A' and car_info.get('link') != 'N/A':
            car_info['location'] = car_info['location'].ljust(20)
            rav4_list.append(car_info)

    return True


# Start scraping from the first page
page_number = 1
url = base_url.format(page_number)
driver.get(url)

while True:
    if not extract_car_data(page_number):
        break

    # Increment page number
    page_number += 1

    # Check if there's a next page
    next_url = base_url.format(page_number)
    driver.get(next_url)

    # Wait until car elements are loaded
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.o-card')))

# Close the browser
driver.quit()

# Print the results
for car in rav4_list:
    print(car)

csv_file = 'rav4_cars.csv'
# csv_file = 'crv_cars.csv'
# CSV 文件的列名
fields = ['title', 'location', 'year', 'odometer', 'price', 'link']

# 写入 CSV 文件
with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fields)

    # 写入列名（header）
    writer.writeheader()

    # 写入每行数据
    for car in rav4_list:
        writer.writerow(car)

print(f"CSV 文件 {csv_file} 写入完成。")







