import streamlit as st
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
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

st.title("Firefox and Geckodriver Installation Verification")
st.write("This app checks if Firefox and Geckodriver are installed correctly.")

st.write("### Directory Contents:")
list_directory_contents("/usr/bin")
list_directory_contents("/usr/local/bin")

st.write("### Paths of Installed Packages:")
execute_command("which firefox || echo 'firefox not found'")
execute_command("firefox --version || echo 'Firefox version check failed'")
execute_command("which geckodriver || echo 'geckodriver not found'")
execute_command("geckodriver --version || echo 'Geckodriver version check failed'")
