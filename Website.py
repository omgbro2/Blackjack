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

# Open group info
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

# Folder where you want to save the images
download_folder = os.path.join(os.getcwd(), "Blackjack", "data")

# Check if the 'data' folder exists, if not create it
if not os.path.exists(download_folder):
    os.makedirs(download_folder)
    print(f"Created folder: {download_folder}")

# Find all the image thumbnails (with background-image style)
thumbnails = driver.find_elements(By.XPATH, '//div[contains(@style, "background-image")]')

for i, thumb in enumerate(thumbnails):
    try:
        thumb.click()
        print(f"Clicked thumbnail {i+1}")
        
        # Wait for the full-size image to load
        full_img = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//img[contains(@src, "https://")]'))
        )
        
        img_url = full_img.get_attribute("src")
        print(f"Image URL: {img_url}")

        # Define the file path to save the image in the 'data' folder
        file_path = os.path.join(download_folder, f"image_{i+1}.jpg")

        # Download the image and save it to the 'data' folder
        img_data = requests.get(img_url).content
        with open(file_path, "wb") as f:
            f.write(img_data)
        print(f"Image {i+1} saved to {file_path}")

        # Look for the close button (you can adjust the XPath to fit)
        try:
            close_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//span[@aria-label="Close"]'))  # Or a close button with specific attributes
            )
            close_button.click()
            print(f"Closed image viewer for image {i+1}")
        except Exception as e:
            print(f"Close button not found for image {i+1}, trying Escape key.")
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)  # Try ESCAPE if no close button found

        time.sleep(1)

    except Exception as e:
        print(f"Failed to get image {i+1}: {e}")
        continue