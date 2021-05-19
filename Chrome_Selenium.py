import time
import os
import difflib
import utils
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from datetime import date

EXTENSION_ID = "chphlpgkkbolifaimnlloiipkdnihall"

USER_PROFILE = os.environ['USERPROFILE']
LOCAL_DESTINATION_PATH = os.path.join(USER_PROFILE, "Documents/OneTab-Backup/")

CHROME_DIR = os.path.join(USER_PROFILE, 'AppData', 'Local', 'Google', 'Chrome')

CHROME_USER_DATA_DIR = os.path.join(CHROME_DIR, 'User Data')
DEFAULT_CHROME_USER_DATA_DIR = os.path.join(
    CHROME_DIR, "User Data", "Default", "Default")

TEMP_DIR = os.path.join(CHROME_DIR, 'temp',)
TEMP_CHROME_USER_DATA = os.path.join(TEMP_DIR, "Default")


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


def create_or_update_backup_file(latestData):
    today = date.today().strftime("%d-%m-%y")
    filename = os.path.join(LOCAL_DESTINATION_PATH, "{}.txt".format(today))

    utils.create_directory_if_not_exists(LOCAL_DESTINATION_PATH)

    if check_need_to_update(LOCAL_DESTINATION_PATH, latestData):
        file = open(filename, 'w', encoding="utf-8")
        file.write(latestData)
        file.close()

        print("Backup Created/Updated")
    else:
        print("No new changes")


utils.copy_directory(DEFAULT_CHROME_USER_DATA_DIR, TEMP_CHROME_USER_DATA)

TEMP_LOCAL_EXTENSION_SETTINGS_EXTENSION_DIR = os.path.join(
    TEMP_CHROME_USER_DATA, "Local Extension Settings", EXTENSION_ID)

utils.copy_all_files_in_directory(os.path.join(CHROME_USER_DATA_DIR, "Default", "Local Extension Settings",
                                  EXTENSION_ID), TEMP_LOCAL_EXTENSION_SETTINGS_EXTENSION_DIR, ["LOCK"])

chrome_options = ChromeOptions()
chrome_options.add_argument(
    "user-data-dir={}".format(TEMP_DIR))
chrome_options.add_extension('./onetab.crx')

driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)
driver.get("chrome-extension://chphlpgkkbolifaimnlloiipkdnihall/import-export.html")

time.sleep(1)  # Let the user actually see something!

contentArea = driver.find_element_by_id("contentAreaDiv")
export_box = driver.find_elements_by_tag_name("textarea")[1]

text = export_box.get_attribute("value")

create_or_update_backup_file(text)

driver.close()
driver.quit()

utils.remove_directory_if_exists(TEMP_DIR)
