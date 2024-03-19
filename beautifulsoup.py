import requests
from bs4 import BeautifulSoup
import time
from urllib.request import urlopen

# Keep track of processed messages using a set
processed_messages = set()

# Function to fetch and process messages
def capture_messages():
    # Replace 'your_website_url' with the actual URL of the website
    url = 'https://web.telegram.org/k/#@team_shadow_current'

    # Send a GET request to the website
    response = requests.get(url)
    page = urlopen(url)
    html = page.read().decode("utf-8")
    # Check if the request was successful (status code 200)
    if html is not None:
        # Parse the HTML content of the page
        soup = BeautifulSoup(html, 'html.parser')
        # print(soup.getText().replace( '\n', ''))
        # Extract messages based on HTML structure
        messages = soup.find_all('div', class_='message spoilers-container')  # Adjust based on actual HTML structure
        print(messages)
        # Process each message
        for message in messages:
            # Extract unique identifier for the message (e.g., message ID or timestamp)
            message_id = message['data-message-id']  # Adjust based on actual HTML structure

            # Check if the message has already been processed
            if message_id not in processed_messages:
                # Extract relevant information (e.g., text, sender, timestamp)
                message_content = message.find('div', class_='message spoilers-container')  # Adjust based on actual HTML structure
                # message_text = message.find('p', class_='message-text').text  # Adjust based on actual HTML structure
                # sender = message.find('span', class_='message-sender').text  # Adjust based on actual HTML structure
                # timestamp = message.find('span', class_='message-timestamp').text  # Adjust based on actual HTML structure

                # Record the message in your desired storage solution (e.g., database, file)
                record_message(message_id, message_text, sender, timestamp)

                # Add the message ID to the set of processed messages
                processed_messages.add(message_id)

    else:
        print(f"Failed to fetch messages. Status code: {response.status_code}")

# Function to record messages (replace with your actual implementation)
def record_message(message_id, message_text, sender, timestamp):
    # Implement your logic to record the message (e.g., store in a database, write to a file)
    # For simplicity, print the message details in this example
    print(f"New message {message_id} from {sender} at {timestamp}: {message_text}")

# Run the script at regular intervals
while True:
    capture_messages()

    # Adjust the sleep duration based on your requirements
    time.sleep(1)  # Sleep for 60 seconds before checking again
