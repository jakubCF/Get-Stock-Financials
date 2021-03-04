import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pathlib
import time
import sys
import signal
import os

# This part handles ctrl+c in command line
def signal_handler(signum, frame):
    print ("Interupted by user\nExit...")
    try:
        driver.close()
        driver.quit()
    except:
        pass
    sys.exit(0)

# Check if files and folder for download exist and create them if now
def depfoldfile():
    open("success.txt", "a")
    open("error.txt", "a")
    if not os.path.exists('download'):
        os.makedirs('download')
    return

def custom_wait(x):
    for i in range(x):
        time.sleep(1)
    return

# Main app
if __name__ == "__main__":
    # ctrl+c calls this line
    signal.signal(signal.SIGINT, signal_handler)

    # Check if files and folders exists and create them if not
    depfoldfile()

    # link "http://financials.morningstar.com/ratios/r.html?t=AAPL&region=NYSE&culture=en_US"

    # GET parameters, region, culture, not important but if stock on different market it might be neccessary
    region = "NYSE"
    culture = "en_US"
    symbol = ""

    link = "http://financials.morningstar.com/balance-sheet/bs.html?t=" + symbol

    # File with list of symbols for which key ratios should be downloaded
    sp500list = "./sp500-symbols-list.csv"

    # Firefox profile for automatic download
    # Path for download is set up to current directory /download, if you change the name, it have to be changed in the func depfoldfile() too.
    folder_path = str(pathlib.Path().absolute()) + "\download"
    profile = webdriver.firefox.options.Options()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", folder_path)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv;text/plain;application/text;text/html")


    # Loads csv with symbols to dataframe
    df = pd.read_csv(sp500list)

    # Set up webdriver with profile
    driver = webdriver.Firefox(options=profile)

    # Loop goes thru all symbols in dataframe, opens website and clicks on button for downloading data
    for symbol in df["Symbol"]:
        wait_login = False
        link = "http://financials.morningstar.com/balance-sheet/bs.html?t=" + symbol
        # Open browser and load page with key ratios for given symbol
        driver.get(link)
        
        # Wait for page to load
        WebDriverWait(driver, 2).until(lambda x: driver.execute_script("return document.readyState")=="complete")

        # Changes period to 10y
        ### ONLY PREMIUM ###
        # Delete or change to 5 for free version
        driver.execute_script("SRT_stocFund.CurrentPeriod(10, this)")

        # Wait for script to finish
        custom_wait(5)

        # Check if you have to login for premium access
        while driver.current_url == "https://www.morningstar.com/sign-up/premium":
            custom_wait(5)
            wait_login = True
        
        # After login we have to load the page again
        if wait_login:
            driver.get(link)
            custom_wait(5)
            driver.execute_script("SRT_stocFund.CurrentPeriod(10, this)")
            custom_wait(5)

        
        # Tries to click button, if not found, exception will catch is and write symbol and exception message to file error.txt
        try:
            driver.execute_script("SRT_stocFund.Export()")
        except Exception as e:
            print(symbol,str(e))
            with open('error.txt', 'a') as file:
                file.write(symbol + ";" + link + ";" + str(e))
            continue
        
        # If there wasn't any exception it was likely successful and adds symbol in success.txt
        with open('success.txt', 'a') as file:
            file.write(symbol + "\n")

        # Little loop for 15 sec pause between opening website. Trying to be little like a human :-D
        custom_wait(15)

    # This should close the window and quit driver instance but for some reason it doesn't work on my win10
    driver.close()
    driver.quit()