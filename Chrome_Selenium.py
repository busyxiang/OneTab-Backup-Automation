import time
import os
import difflib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from datetime import date

# Make sure no chrome is open when run the script!!


def create_directory_if_not_exists(dirPath):
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)


def check_need_to_update(dirPath, latestData):
    if os.path.exists(dirPath) and len(os.listdir(dirPath)) > 0:
        files = os.listdir(dirPath)
        lastUpdateFile = open(os.path.join(
            dirPath, files[-1]), 'r', encoding="utf-8")

        diffResult = difflib.Differ().compare(lastUpdateFile.read(), latestData)

        # List Comprehension
        return [x for x in diffResult if x[0] in ('+', '-')]
    else:
        return True


USER_PROFILE = os.environ['USERPROFILE']
LOCAL_DESTINATION_PATH = os.path.join(USER_PROFILE, "Documents/OneTab-Backup/")

chrome_options = ChromeOptions()
chrome_options.add_argument(
    "user-data-dir=C:\\Users\\busyx\AppData\\Local\\Google\\Chrome\\User Data")

# DONT DO this if you are accessing your own user date, the extension will be missing after the test
# Havent figure out why
# chrome_options.add_extension('./onetab.crx')

driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)
driver.get("chrome-extension://chphlpgkkbolifaimnlloiipkdnihall/import-export.html")

contentArea = driver.find_element_by_id("contentAreaDiv")
export_box = driver.find_elements_by_tag_name("textarea")[1]

time.sleep(2)  # Let the user actually see something!

text = export_box.get_attribute("value")

date = date.today().strftime("%d-%m-%y")
filename = os.path.join(LOCAL_DESTINATION_PATH, "{}.txt".format(date))

create_directory_if_not_exists(LOCAL_DESTINATION_PATH)

if check_need_to_update(LOCAL_DESTINATION_PATH, text):
    file = open(filename, 'w', encoding="utf-8")
    file.write(text)
    file.close()

    print("Backup Created/Updated")
else:
    print("No new changes")

driver.quit()
