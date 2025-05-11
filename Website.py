from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
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

#Wait to sync media
try:
    print("Waiting for WhatsApp to finish syncing older messages...")
    # Wait until the sync message appears
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Syncing older messages.")]'))
    )
    # Then wait for it to disappear (sync complete)
    WebDriverWait(driver, 60).until_not(
        EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Syncing older messages.")]'))
    )
    print("Sync complete. Refreshing page...")
    #refresh the page so it truly loads
    driver.refresh()
except Exception as e:
    print(f"Sync message not detected or error occurred: {e}")

#Confirms that the page has refreshed
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//img[contains(@src, 'cdn.whatsapp.net')]")
        )
    )
    print("Page refreshed")
    print("Waiting for anti-macro")
    time.sleep(10)
except TimeoutException:
    print("Refresh failed")

#Opens the blackjack group 2nd time
print("finding group")
group_name = "Black balance blackjack"
group = driver.find_element(By.XPATH, f'//span[contains(@title, "{group_name}")]')
group.click()
print("Chat opened 2")

#Open group info 2nd time
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f'//div[@id="main"]//span[contains(text(), "{group_name}")]'))
    )
    element.click()
    print("info opened 2")
except:
    print("info Not found 2")

#Open media gallery 2nd time
try:
    media_tab = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH,'//div[contains(@class, "x1fcty0u") and contains(text(), "Media")]')))
    media_tab.click()
    print("Media clicked 2")
except:
    print("Media not found 2")

#Create the data folder to store images
download_folder = os.path.join(os.getcwd(), "Blackjack", "data")
if not os.path.exists(download_folder):
    os.makedirs(download_folder)
    print(f"Created folder: {download_folder}")

#Wait for the media dialog to appear
dialog = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "dialog")]'))
)

#Find all items with role="listitem" inside the dialog
media_items = dialog.find_elements(By.XPATH, './/*[@role="listitem"]')

#Click the first item
if media_items:
    media_items[1].click()
    print("Clicked the first media item.")
else:
    print("No media items found to click.")

time.sleep(30)