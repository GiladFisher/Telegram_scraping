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
    print(message)
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

def load_random_file_to_clipboard(mean_size):
    std = mean_size / 2
    message_size = -1
    file_path = 'random_file.bin'
    while message_size < 0:
        message_size = int(np.random.normal(mean_size, std) * 1024**2)
    print(f"Generating a random file of size {message_size} bytes, in KB: {message_size / 1024}, in MB: {message_size / (1024**2)}")
    with open(file_path, 'wb') as file:
        file.write(os.urandom(message_size))
    command = f"powershell Set-Clipboard -LiteralPath {file_path}"
    os.system(command)

# Function to generate a random message
def generate_random_message():
    global message_type
    # Define probabilities for each type of message
    text_prob = 0.356  # Probability of generating a text message
    image_prob = 0.581  # Probability of generating an image
    video_prob = 0.113  # Probability of generating a video
    voice_prob = 0.061  # Probability of generating a voice recording

    # Generate a random number to determine the type of message
    rand_num = random.random()

    # Generate and return the corresponding content based on the randomly chosen type
    if rand_num < text_prob:
        message_type = 'text'
        return generate_random_text()

    elif rand_num < text_prob + image_prob:
        message_type = 'image'
        load_random_noise_image_to_clipboard()
        return None

    else:
        message_type = 'voice'
        load_random_voice_message_to_clipboard()
        return None


# # Define probabilities for each type of message
    # text_prob = 0.29  # Probability of generating a text message
    # image_prob = 0.48 # Probability of generating an image
    # video_prob = 0.15  # Probability of generating a video
    # voice_prob = 0.05 # Probability of generating a voice recording
    # file_prob = 0.02  # Probability of generating
    #
    # # Generate a random number to determine the type of message
    # rand_num = random.random()
    #
    # # Generate and return the corresponding content based on the randomly chosen type
    # if rand_num < text_prob:
    #     message_type = 'text'
    #     mean_size = 306.61 / (1024**2)  # 306 B in MB
    #
    # elif rand_num < text_prob + image_prob:
    #     message_type = 'image'
    #     mean_size = 91.33 / (1024)
    #
    # elif rand_num < text_prob + image_prob + voice_prob:
    #     message_type = 'voice'
    #     mean_size = 4.4 # 0.5 MB in bytes
    #
    # elif rand_num < text_prob + image_prob + voice_prob + file_prob:
    #     message_type = 'file'
    #     mean_size = 52.56 / 1024 # 52.56 KB in MB
    #
    # else:
    #     message_type = 'video'
    #     mean_size = 35.49 # 35.49 MB
    #
    # load_random_file_to_clipboard(mean_size)
    # return None

def generate_random_text():
    global message_size
    message_length = max(min(round(random.expovariate(1/20) + 80), 1120), 1)  # Random message length
    message = ''.join(random.choices(string.ascii_letters + string.digits, k=message_length))
    message_size = sys.getsizeof(message)
    return message
# Function to send a random message in the chat
def send_random_message(driver):
    global message_type
    global message_size
    message = generate_random_message()
    input_box = driver.find_element(By.XPATH, '//*[@id="column-center"]/div/div/div[4]/div/div[4]/button[1]')

    if message is not None:
        # Simulate typing the message using ActionChains
        ActionChains(driver).click(input_box).key_down(Keys.CONTROL).send_keys('a').send_keys(Keys.BACKSPACE).key_up(Keys.CONTROL).send_keys(message).send_keys(Keys.ENTER).perform()
    else:
        ActionChains(driver).click(input_box).key_down(Keys.CONTROL).send_keys('a').send_keys(Keys.BACKSPACE).send_keys('v').key_up(Keys.CONTROL).send_keys(Keys.ENTER).perform()
        time.sleep(1)
        ActionChains(driver).send_keys(Keys.ENTER).perform()

    epoch_time = time.time()
    # Record the message size and time
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([epoch_time, message_size, message_type])
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
        #ActionChains(driver).click(input_box).key_down(Keys.CONTROL).send_keys('a').send_keys(Keys.BACKSPACE).key_up(Keys.CONTROL).send_keys(Keys.ENTER).perform()
        time.sleep(min(random.expovariate(1/60) + 60, 600))  # Random time interval between messages

# Run the script
# create a new csv file
currtime = time.strftime("%Y%m%d-%H%M%S")
filename = "telegram_messages" + currtime + ".csv"
with open(filename, mode='w', newline='') as file:
    # Create a CSV writer object
    writer = csv.writer(file)

    # Write the header row
    header = ["time", "size", "message_type"]
    writer.writerow(header)

    # close the file
    file.close()
simulate_random_messages()
