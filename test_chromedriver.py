import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import chromedriver_autoinstaller
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

st.title("Chromium and ChromeDriver Installation Verification")
st.write("This app checks if Chromium and ChromeDriver are installed correctly.")

st.write("### Directory Contents:")
list_directory_contents("/usr/bin")
list_directory_contents("/usr/local/bin")

st.write("### Paths of Installed Packages:")
execute_command("which chromium-browser || echo 'chromium-browser not found'")
execute_command("/usr/local/bin/chromium-browser --version || echo 'chromium-browser version check failed'")

st.write("### Testing ChromeDriver:")
chromedriver_autoinstaller.install()
chrome_options = ChromeOptions()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

try:
    driver = webdriver.Chrome(service=ChromeService(), options=chrome_options)
    driver.get("https://www.google.com")
    st.write(f"Page title: {driver.title}")
    driver.quit()
except Exception as e:
        st.error(f"Error: {e}")
