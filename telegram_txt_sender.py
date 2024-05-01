from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import string

# Function to generate a random message
def generate_random_message():
    message_length = random.randint(5, 50)  # Random message length
    message = ''.join(random.choices(string.ascii_letters + string.digits, k=message_length))
    return message

# Function to send a random message in the chat
def send_random_message(driver):
    message = generate_random_message()
    input_box = driver.find_element(By.XPATH, '//div[@class="composer_rich_textarea"]')
    input_box.send_keys(message)
    input_box.send_keys('\n')

# Function to scroll to the bottom of the chat window
def scroll_to_bottom(driver):
    # This is just an example XPath, adjust it based on your chat window structure
    scrollable_div = driver.find_element(By.XPATH, '//div[@class="history"]')
    driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", scrollable_div)

# Main function to simulate sending random messages
def simulate_random_messages():
    url = 'https://web.telegram.org/k/#6983010885'  # Replace with your chat URL
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(10)  # Allow time for the page to load

    while True:
        send_random_message(driver)
        time.sleep(random.uniform(2, 5))  # Random time interval between messages
        scroll_to_bottom(driver)  # Scroll to bottom after sending each message

# Run the script
simulate_random_messages()
