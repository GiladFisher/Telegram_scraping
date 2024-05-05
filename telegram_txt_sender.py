import os
import sys
import cv2
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random
import string
import csv
import numpy as np

def load_random_noise_image_to_clipboard():
    # Define target average size in bytes
    target_average_size = 91.33 * 1024  # Convert KB to bytes

    # Generate random width and height within a reasonable range
    width = np.random.randint(64, 512)
    height = np.random.randint(64, 512)

    # Calculate the target size for the image
    target_size = np.random.uniform(2400, 378680)  # Random size between 2.40KB and 378.68KB

    # Calculate the scale factor to achieve the target size
    scale_factor = np.sqrt(target_size / (width * height * 3))

    # Generate random noise using OpenCV with adjusted scale factor
    noise = np.random.randint(0, 256, (int(height * scale_factor), int(width * scale_factor), 3), dtype=np.uint8)

    # Resize the noise image to the original size
    noise = cv2.resize(noise, (width, height), interpolation=cv2.INTER_LINEAR)

    # Save the image to a PNG file
    image_path = 'random_noise_image.png'
    cv2.imwrite(image_path, noise)

    # Load the image to the clipboard using PowerShell
    command = f"powershell Set-Clipboard -LiteralPath {image_path}"
    os.system(command)


# Function to generate a random message
def generate_random_message():
    # Define probabilities for each type of message
    text_prob = 0.294  # Probability of generating a text message
    image_prob = 0.48  # Probability of generating an image
    video_prob = 0.113  # Probability of generating a video
    voice_prob = 0.113  # Probability of generating a voice recording

    # Generate a random number to determine the type of message
    rand_num = random.random()

    # Generate and return the corresponding content based on the randomly chosen type
    if rand_num < text_prob:
        return generate_random_text()
    elif rand_num < text_prob + image_prob:
        return load_random_noise_image_to_clipboard()
    # elif rand_num < text_prob + image_prob + video_prob:
    #     return generate_random_video()
    # else:
    #     return generate_random_voice_recording()


def generate_random_text():
    message_length = min(round(random.expovariate(1/20)), 120)  # Random message length
    message = ''.join(random.choices(string.ascii_letters + string.digits, k=message_length))
    return message
# Function to send a random message in the chat
# //*[@id="column-center"]/div/div/div[4]/div/div[4]/button[1]
def send_random_message(driver):
    message = generate_random_message()
    input_box = driver.find_element(By.XPATH, '//*[@id="column-center"]/div/div/div[4]/div/div[4]/button[1]')

    if type(message) == str:
        # Simulate typing the message using ActionChains
        ActionChains(driver).click(input_box).key_down(Keys.CONTROL).send_keys('a').send_keys(Keys.BACKSPACE).key_up(Keys.CONTROL).send_keys(message).send_keys(Keys.ENTER).perform()
    else:
        ActionChains(driver).click(input_box).key_down(Keys.CONTROL).send_keys('a').send_keys(Keys.BACKSPACE).send_keys('v').key_up(Keys.CONTROL).send_keys(Keys.ENTER).perform()
        time.sleep(1)
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
        time.sleep(min(random.expovariate(1/60), 120))  # Random time interval between messages

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
