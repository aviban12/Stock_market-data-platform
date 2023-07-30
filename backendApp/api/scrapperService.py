from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import json
import re
import threading
import schedule

def checkIfExsists(stockId):
    url = "http://localhost:8000/get-stocks/{}/".format(stockId)

    headers = {
    'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        return True
    else:
        return False

def updateData(stockId, data):
    url = "http://localhost:8000/update-stock/{}/".format(stockId)

    payload = json.dumps(data)

    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    return True

# Send post request to the Django API
def sendPostRequest(data):
    doesExists = checkIfExsists(data['stock_id'])
    if doesExists:
        updateData(data['stock_id'], data)
        return True

    url = "http://localhost:8000/create-stock/"

    payload = json.dumps(data)
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return True

# Function to scroll to the bottom of the page
def scroll_to_bottom(scroll_times, driver):
    scrollHeight = 1000
    for _ in range(scroll_times):
        driver.execute_script("window.scrollTo(0, "+ str(scrollHeight) +")")
        scrollHeight += 1000
        time.sleep(1)


def startRendering(pageNumber):
    print("API called for Page Number = {}".format(pageNumber))
    # Configure the headless browser options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--window-size=1920x1080")  # Set window size

    # Initialize the web driver with the configured options
    driver = driver = webdriver.Firefox(chrome_options)

    # Open the URL of the lazy-loaded page
    url = 'https://coinmarketcap.com/?page={}'.format(pageNumber)
    driver.get(url)

    # Define the number of times to scroll to load more data
    scroll_times = 7

    # Scroll to the bottom of the page to load more data
    scroll_to_bottom(scroll_times, driver)

    # Get the page source using Selenium
    page_source = driver.page_source

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    rows1_100 = []
    # Extract and print the data using BeautifulSoup
    cryptocurrencies = soup.find_all('table', class_='cmc-table')

    for row in cryptocurrencies:
        data = row.find_all('td')
        rows1_100 = [cell.text.strip() for cell in data]

    startIndexToFetch = 0
    lastIndexToFetch = 11
    totalDataToInsert = []
    insertedDataCount = 0
    # numbers = re.findall(r'[MB]?(\d+)', data)
    for index in range(len(rows1_100)//11):
        try:
            currentRowsToInsert = rows1_100[startIndexToFetch:lastIndexToFetch]
            currentDictToUpdateInDB = {}
            marketCap = currentRowsToInsert[7]
            currentDictToUpdateInDB['stock_id'] = int(currentRowsToInsert[1])
            currentDictToUpdateInDB['name'] = currentRowsToInsert[2]
            currentDictToUpdateInDB['price'] = currentRowsToInsert[3]
            currentDictToUpdateInDB['percent_change_1hr'] = currentRowsToInsert[4]
            currentDictToUpdateInDB['percent_change_24hr'] = currentRowsToInsert[5]
            currentDictToUpdateInDB['percent_change_7d'] = currentRowsToInsert[6]
            currentDictToUpdateInDB['volume_24h'] = currentRowsToInsert[8]
            currentDictToUpdateInDB['current_supply'] = currentRowsToInsert[9]
            findMOrBIndex = marketCap.find('M')
            if findMOrBIndex > 0:
                currentDictToUpdateInDB['market_cap'] = marketCap[findMOrBIndex+1:]
            else:
                findMOrBIndex = marketCap.find('B')
                currentDictToUpdateInDB['market_cap'] = marketCap[findMOrBIndex+1:]
            try:
                stockPushAPICall = threading.Thread(target=sendPostRequest, args=(currentDictToUpdateInDB,))
                stockPushAPICall.start()
                insertedDataCount += 1
            except:
                pass
            startIndexToFetch += 11
            lastIndexToFetch += 11
        except Exception as exception:
            print(exception)

    # Close the web driver
    driver.quit()
