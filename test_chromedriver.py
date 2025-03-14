import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import os

def test_chromedriver():
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Set the path to the Chrome binary
    chrome_binary_path = "/usr/bin/google-chrome"
    if os.path.exists(chrome_binary_path):
        chrome_options.binary_location = chrome_binary_path
    else:
        st.error(f"Chrome binary not found at {chrome_binary_path}")
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
