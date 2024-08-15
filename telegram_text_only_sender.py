import os
import sys
from moviepy.editor import VideoFileClip
import cv2
from gtts import gTTS
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random
import string
import csv
import numpy as np

message_type = ''
message_size = 0

def estimate_duration_for_size(target_size):
    input_file = 'video.mp4'
    video_clip = VideoFileClip(input_file)
    original_duration = video_clip.duration
    original_size = os.path.getsize(input_file)
    target_duration = original_duration * (target_size / original_size)
    return target_duration

def load_random_video_to_clipboard():
    global message_size
    # target_size = int(np.random.normal(35.4 * 1024 * 1024, 5 * 1024 * 1024))  # Standard deviation of 5 MB
    # # Define target size in bytes
    # target_size = 35.4 * 1024 * 1024  # 35.4 MB in bytes
    # input_file = 'video.mp4'
    # output_file = 'trimmed_video.mp4'
    # video_clip = VideoFileClip(input_file)
    # duration = estimate_duration_for_size(target_size)
    # duration = int(np.random.normal(100, 10))
    # trimmed_clip = video_clip.subclip(0, duration)
    # trimmed_clip.write_videofile(output_file, codec="libx264", threads=4)
    output_file = 'random_video.mp4'
    message_size = os.path.getsize(output_file)
    # Load the video to the clipboard using PowerShell
    command = f"powershell Set-Clipboard -LiteralPath {output_file}"
    os.system(command)

def load_random_voice_message_to_clipboard():
    global message_size
    message = generate_random_text()
    tts = gTTS(text=message, lang='en')
    voice_path = 'random_message.mp3'
    tts.save(voice_path)
    message_size = os.path.getsize(voice_path)
    command = f"powershell Set-Clipboard -LiteralPath {voice_path}"
    os.system(command)

def load_random_noise_image_to_clipboard():
    global message_size
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

    message_size = os.path.getsize(image_path)

    # Load the image to the clipboard using PowerShell
    command = f"powershell Set-Clipboard -LiteralPath {image_path}"
    os.system(command)


# Function to generate a random message
def generate_random_message():
    # random choice of characters
    objects = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
               'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ', Keys.ENTER]
    selected_object = random.choice(objects)
    return selected_object




def generate_random_text():
    global message_size
    message_length = min(round(random.expovariate(1/20)), 120)  # Random message length
    message = ''.join(random.choices(string.ascii_letters + string.digits, k=message_length))
    message_size = sys.getsizeof(message)
    return message
# Function to send a random message in the chat
# //*[@id="column-center"]/div/div/div[4]/div/div[4]/button[1]
def send_random_message(driver):
    message = generate_random_message()
    input_box = driver.find_element(By.XPATH, '//*[@id="message-input-text"]/div[1]/div')

    if message is Keys.ENTER:
        message_type = 'Enter'
    else:
        message_type = 'Char'

    ActionChains(driver).click(input_box).send_keys(message).perform()


    epoch_time = time.time()
    # Record the message size and time
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([epoch_time, message_type])
        file.close()

# Function to scroll to the bottom of the chat window

# Main function to simulate sending random messages
def simulate_random_messages():
    url = 'https://web.telegram.org/a/#-4181877490'  # Replace with your chat URL
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(25)  # Allow time for the page to load

    while True:
        send_random_message(driver)
        time.sleep(min(random.expovariate(1/30), 120))  # Random time interval between messages

# Run the script
# create a new csv file
currtime = time.strftime("%Y%m%d-%H%M%S")
filename = "telegram_messages" + currtime + ".csv"
with open(filename, mode='w', newline='') as file:
    # Create a CSV writer object
    writer = csv.writer(file)

    # Write the header row
    header = ["time", "message_type"]
    writer.writerow(header)

    # close the file
    file.close()
simulate_random_messages()