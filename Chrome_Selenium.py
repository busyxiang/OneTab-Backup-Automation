import time
import os
import difflib
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from datetime import date
from utils import create_directory_if_not_exists, remove_directory_if_exists

# Make sure no chrome is open when run the script!!
USER_PROFILE = os.environ['USERPROFILE']
LOCAL_DESTINATION_PATH = os.path.join(USER_PROFILE, "Documents/OneTab-Backup/")
CHROME_USER_DATA = os.path.join(
    'AppData', 'Local', 'Google', 'Chrome', 'User Data')
CLONE_CHROME_USER_DATA = os.path.join(
    'AppData', 'Local', 'Google', 'Chrome', 'temp')


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


def create_copy_of_user_data():
    src = os.path.join(USER_PROFILE, CHROME_USER_DATA)
    dest = os.path.join(USER_PROFILE, CLONE_CHROME_USER_DATA)

    shutil.copytree(src, dest)


def create_or_update_backup_file(latestData):
    today = date.today().strftime("%d-%m-%y")
    filename = os.path.join(LOCAL_DESTINATION_PATH, "{}.txt".format(today))

    create_directory_if_not_exists(LOCAL_DESTINATION_PATH)

    if check_need_to_update(LOCAL_DESTINATION_PATH, latestData):
        file = open(filename, 'w', encoding="utf-8")
        file.write(text)
        file.close()

        print("Backup Created/Updated")
    else:
        print("No new changes")


def backup_method_1():
    chrome_options = ChromeOptions()
    chrome_options.add_argument(
        "user-data-dir={}".format(os.path.join(USER_PROFILE, CHROME_USER_DATA)))

    return webdriver.Chrome('chromedriver.exe', options=chrome_options)


# Still need to figure out a better way, copy 'User Data' folder takes very long
def backup_method_2():
    create_copy_of_user_data()

    chrome_options = ChromeOptions()
    chrome_options.add_argument(
        "user-data-dir={}".format(os.path.join(USER_PROFILE, CLONE_CHROME_USER_DATA)))

    return webdriver.Chrome('chromedriver.exe', options=chrome_options)

# DONT DO this if you are accessing your own user date, the extension will be missing after the test
# Havent figure out why
# chrome_options.add_extension('./onetab.crx')


driver = backup_method_1()
driver.get("chrome-extension://chphlpgkkbolifaimnlloiipkdnihall/import-export.html")

time.sleep(1)  # Let the user actually see something!

contentArea = driver.find_element_by_id("contentAreaDiv")
export_box = driver.find_elements_by_tag_name("textarea")[1]

text = export_box.get_attribute("value")

create_or_update_backup_file(text)

driver.close()
driver.quit()

# remove_directory_if_exists(os.path.join(USER_PROFILE, CLONE_CHROME_USER_DATA))
