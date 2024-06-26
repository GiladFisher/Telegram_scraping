from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re # Import the regular expression module

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
