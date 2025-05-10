from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import requests
import time
import os


#Opens whatsapp in a new browser to be clean.
driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com")

#Confirms that the Login has been completed
try:
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located(
            (By.XPATH, "//img[contains(@src, 'cdn.whatsapp.net')]")
        )
    )
    print("Logged in")
except TimeoutException:
    print("Login timeout")
    driver.quit()
    
#Closes any pop-up
try:
    WebDriverWait(driver, 10, poll_frequency=1).until(
        EC.element_to_be_clickable((By.XPATH, '//button//div[contains(text(), "Continue")]'))
    )
    # Once clickable, click it
    continue_btn = driver.find_element(By.XPATH, '//button//div[contains(text(), "Continue")]')
    continue_btn.click()
except NoSuchElementException:
    print("No popup found. Continuing...")
except TimeoutException:
    print("No popup found. Continuing...")

#Opens the blackjack group
group_name = "Black balance blackjack"
group = driver.find_element(By.XPATH, f'//span[contains(@title, "{group_name}")]')
group.click()
print("Chat opened")

#Open group info
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f'//div[@id="main"]//span[contains(text(), "{group_name}")]'))
    )
    element.click()
    print("info opened")
except:
    print("info Not found")

#Open media gallery
try:
    media_tab = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH,'//div[contains(@class, "x1fcty0u") and contains(text(), "Media")]')))
    media_tab.click()
    print("Media clicked")
except:
    print("Media not found")


#Download the pictures

#Create the folder path
download_folder = os.path.join(os.getcwd(), "Blackjack", "data")
if not os.path.exists(download_folder):
    os.makedirs(download_folder)
    print(f"Created folder: {download_folder}")

#Wait for the dialog with media items to appear
dialog = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@role="dialog"]'))
)

#Find all media and video items
try:
    media_items = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located(By.XPATH, './/*[@aria-label="image" or @aria-label="video"]'))
except TimeoutException:
    print("No media items (images or videos) found within 20 seconds. Exiting.")
    driver.quit()

#How many items to scroll through to download
total_items = len(media_items)
print(f"Found {total_items} media items")

if total_items > 0:
    media_items[0].click()  #Click the first media item
    print("Clicked first image")
    time.sleep(10)

    for i in range(total_items):
        try:
            #Wait for image to load
            full_img = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//img[contains(@src, "https://")]'))
            )
            img_url = full_img.get_attribute("src")
            print(f"[{i+1}/{total_items}] Image URL: {img_url}")

            file_path = os.path.join(download_folder, f"image_{i+1}.jpg")
            img_data = requests.get(img_url).content
            with open(file_path, "wb") as f:
                f.write(img_data)
            print(f"Saved image to {file_path}")

            # TODO: Add code to locate and click the "Next" button here
            # Example placeholder:
            # next_button = driver.find_element(By.XPATH, '//button[@aria-label="Next"]')
            # next_button.click()
            # print("Clicked next button")

            time.sleep(1)

        except Exception as e:
            print(f"Error processing item {i+1}: {e}")
            break
else:
    print("No media items found.")