import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import os
import subprocess

def list_directory_contents(directory):
    try:
        contents = subprocess.check_output(["ls", directory]).decode("utf-8")
        st.text(contents)
    except Exception as e:
        st.error(f"Error listing contents of {directory}: {e}")

def execute_command(command):
    try:
        output = subprocess.check_output(command, shell=True).decode("utf-8")
        st.text(output)
    except Exception as e:
        st.error(f"Error executing command '{command}': {e}")

def test_chromedriver():
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Use the CHROME_BIN environment variable to locate the Chrome binary
    chrome_binary_path = os.getenv("CHROME_BIN")
    if chrome_binary_path and os.path.exists(chrome_binary_path):
        chrome_options.binary_location = chrome_binary_path
        st.write(f"Using Chrome binary at: {chrome_binary_path}")
    else:
        st.error("Chrome binary not found. Listing /usr/bin, /usr/local/bin, and /opt/google/chrome directories for debugging:")
        list_directory_contents("/usr/bin")
        list_directory_contents("/usr/local/bin")
        list_directory_contents("/opt/google/chrome")
        st.write("Checking paths of installed packages:")
        execute_command("which chromium-browser")
        execute_command("which chromedriver")
        execute_command("which google-chrome")
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
