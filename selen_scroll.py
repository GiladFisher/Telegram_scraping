from selenium import webdriver
import time

# Set up Selenium webdriver (ensure you have downloaded the appropriate browser driver)
driver = webdriver.Chrome()

# Open the webpage
driver.get('https://web.telegram.org/k/#@team_shadow_current')

# Define a function to scroll the page to the top
def scroll_to_top(driver):
    driver.execute_script("window.scrollTo(0, 0);")

# Define a function to scroll to the bottom
def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Get initial page height
last_height = driver.execute_script("return document.body.scrollHeight")

# Record initial content
initial_content = driver.page_source

# Scroll to the top to start recording new content
scroll_to_top(driver)

# Loop to scroll and record new content
while True:
    # Scroll to the bottom to load new content
    scroll_to_bottom(driver)

    # Wait for new content to load
    time.sleep(25)  # Adjust the delay time as needed

    # Get new page height
    new_height = driver.execute_script("return document.body.scrollHeight")

    # Record new content if page height has changed
    if new_height != last_height:
        new_content = driver.page_source

        # Save or process new content as needed
        # Example: You can save the content to a file
        with open("new_content.html", "w", encoding="utf-8") as file:
            file.write(new_content)

        # Update last height
        last_height = new_height
    else:
        # If no new content is loaded, break the loop
        break

# Remember to close the browser window when done
driver.quit()
