from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
import time
import re # Import the regular expression module

def scroll_to_top(driver):
    element = driver.find_element(By.CLASS_NAME, 'scrollable-thumb')
    element = driver.find_element(By.XPATH, '//*[@id="column-center"]/div/div/div[3]/div[2]/div[2]/section/div[4]')
    # # "//*[@id='column-center']")
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    # driver.execute_script("window.scrollBy(0,-500);")
    # element = driver.find_element_by_id("your_element_id_here")  # Replace "your_element_id_here" with the ID of your element
    #
    # # Create an ActionChains object
    # actions = ActionChains(driver)
    #
    # # Click, hold, and move the element up by a few pixels
    # actions.move_to_element(element).click_and_hold(element).move_by_offset(0, -50).release().perform()

# Keep track of processed messages using a set
processed_messages = set()

# Function to fetch and process messages using Selenium
def capture_messages():
    # Replace 'your_website_url' with the actual URL of the website
    url = 'https://web.telegram.org/k/#@team_shadow_current'



    # Set up Chrome driver (you may need to download chromedriver.exe and specify its path)
    driver = webdriver.Chrome()

    # Navigate to the website
    driver.get(url)

    # Allow some time for dynamic content to load (you may need to adjust this)
    time.sleep(43)
    while True:
        # Extract messages based on HTML structure using Selenium
        messages = driver.find_elements(By.CLASS_NAME, 'bubbles-group')  # Adjust based on actual HTML structure

        print(len(messages))
        # Process each message
        for message in messages:

            message = message.get_attribute('innerHTML')
            message_id = re.search(r'<div data-mid="(\d+)"', message).group(1)

            # Extract unique identifier for the message (e.g., message ID or timestamp)
            # Check if the message has already been processed
            if message_id not in processed_messages:
                # Extract relevant information within the nested div
                if get_reply(message) is not None:
                    message_text = re.search(r'</div></div></div>(.*?)<span class="time is-block">', message)
                else:  # If it's not a reply, extract the message text directly
                    message_text = re.search(r'<div class="message spoilers-container" dir="auto">(.*?)<', message)

                if message_text is not None:
                    message_text = message_text.group(1)
                # pattern = re.compile(r'<div class="bubble-content"[^>]*>.*?<span class="peer-title"[^>]*>(.*?)</span>.*?<div class="reply-subtitle"[^>]*>(.*?)</div>', re.DOTALL)
                # message_text = re.findall(pattern, message)

                sender = re.search(r'<div class="colored-name[^>]*><span[^>]*>(.*?)</span>', message)
                if sender is None:
                    sender = "Unknown"
                else:
                    sender = sender.group(1)
                timestamp = re.search(r'data-timestamp="(\d+)"', message).group(1)
                # Record the message in your desired storage solution
                record_message(message_id, message_text, sender, timestamp)

                # Add the message ID to the set of processed messages
                processed_messages.add(message_id)
        time.sleep(1)
        scroll_to_top(driver)
        # last_height = driver.execute_script("return document.body.scrollHeight")
        # while True:
        #     driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        #     time.sleep(0.5)
        #     new_height = driver.execute_script("return document.body.scrollHeight")
        #     if new_height == last_height:
        #         break
        #
        #     last_height = new_height
        time.sleep(5)
        # Close the browser
    driver.quit()

# Function to record messages (replace with your actual implementation)
def record_message(message_id, message_text, sender, timestamp):
    # Implement your logic to record the message (e.g., store in a database, write to a file)
    # For simplicity, print the message details in this example

    print(f"New message {message_id} from {sender} at {timestamp}: {message_text}")
def get_reply(message):
    if re.search(r'<div class="reply-content"(.*?)</div></div></div>', message) is not None:
        return re.search(r'<div class="reply-content"(.*?)</div></div></div>', message).group(1)
    else:
        return None
# Run the script at regular intervals
while True:
    capture_messages()

    # Adjust the sleep duration based on your requirements
    time.sleep(30)  # Sleep for 60 seconds before checking again
