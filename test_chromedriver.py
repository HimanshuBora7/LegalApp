import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import os
import subprocess

def list_directory_contents(directory):
    try:
        contents = subprocess.check_output(["ls", directory]).decode("utf-8")
        st.text(contents)
    except Exception as e:
        st.error(f"Error listing contents of {directory}: {e}")

def find_chrome_binary():
    paths_to_check = ["/usr/bin/google-chrome", "/usr/bin/chromium-browser", "/usr/bin/chromium"]
    for path in paths_to_check:
        if os.path.exists(path):
            return path
    return None

def test_chromedriver():
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Dynamically find the Chrome binary path
    chrome_binary_path = find_chrome_binary()
    if chrome_binary_path:
        chrome_options.binary_location = chrome_binary_path
        st.write(f"Using Chrome binary at: {chrome_binary_path}")
    else:
        st.error("Chrome binary not found. Listing /usr/bin and /usr/local/bin directories for debugging:")
        list_directory_contents("/usr/bin")
        list_directory_contents("/usr/local/bin")
        return

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    try:
        driver.get("https://www.google.com")
        title = driver.title
        st.write(f"Page title: {title}")
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        driver.quit()

st.title("Chrome WebDriver Test")
st.write("Click the button below to test if Chrome WebDriver is working correctly.")

if st.button("Run WebDriver Test"):
    test_chromedriver()
