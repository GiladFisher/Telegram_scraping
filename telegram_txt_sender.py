import sys

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random
import string
import csv

# Function to generate a random message
def generate_random_message():
    message_length = random.randint(5, 50)  # Random message length
    message = ''.join(random.choices(string.ascii_letters + string.digits, k=message_length))
    return message

# Function to send a random message in the chat
# //*[@id="column-center"]/div/div/div[4]/div/div[4]/button[1]
def send_random_message(driver):
    message = generate_random_message()
    input_box = driver.find_element(By.XPATH, '//*[@id="column-center"]/div/div/div[4]/div/div[4]/button[1]')

    # Simulate typing the message using ActionChains
    ActionChains(driver).click(input_box).send_keys(message).perform()
    # Simulate pressing Enter key
    ActionChains(driver).send_keys(Keys.ENTER).perform()
    epoch_time = time.time()
    # Record the message size and time
    size = sys.getsizeof(message)
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([epoch_time, size])
        file.close()

# Function to scroll to the bottom of the chat window

# Main function to simulate sending random messages
def simulate_random_messages():
    url = 'https://web.telegram.org/k/#-2083791908'  # Replace with your chat URL
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(25)  # Allow time for the page to load

    while True:
        send_random_message(driver)
        time.sleep(random.uniform(2, 5))  # Random time interval between messages

# Run the script
# create a new csv file
currtime = time.strftime("%Y%m%d-%H%M%S")
filename = "telegram_messages" + currtime + ".csv"
with open(filename, mode='w', newline='') as file:
    # Create a CSV writer object
    writer = csv.writer(file)

    # Write the header row
    header = ["time", "size"]
    writer.writerow(header)

    # close the file
    file.close()
simulate_random_messages()
