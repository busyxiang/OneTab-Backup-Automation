import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from datetime import date

# Make sure no chrome is open when run the script!!

PATH = "C:\Program Files (x86)\chromedriver.exe"
DESTINATION_PATH = "C:/Users/busyx/Documents/OneTab-Backup/"

chrome_options = ChromeOptions()
chrome_options.add_argument(
    "user-data-dir=C:\\Users\\busyx\AppData\\Local\\Google\\Chrome\\User Data")

# DONT DO this if you are accessing your own user date, the extension will be missing after the test
# chrome_options.add_extension('./onetab.crx')

# Optional argument, if not specified will search path.
driver = webdriver.Chrome(PATH, options=chrome_options)
driver.get("chrome-extension://chphlpgkkbolifaimnlloiipkdnihall/import-export.html")

contentArea = driver.find_element_by_id("contentAreaDiv")
export_box = driver.find_elements_by_tag_name("textarea")[1]

time.sleep(2)  # Let the user actually see something!

text = export_box.get_attribute("value")

# Debug
# for box in export_box:
#     print(box)
#     print(box.get_attribute("value"))

date = date.today().strftime("%d-%m-%y")
filename = DESTINATION_PATH + date + ".txt"

dirname = os.path.dirname(filename)
if not os.path.exists(dirname):
    os.makedirs(dirname)

file = open(filename, 'w', encoding="utf-8")
file.write(text)
file.close()

driver.quit()
