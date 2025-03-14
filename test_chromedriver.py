import streamlit as st
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
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

st.title("Microsoft Edge and Edge WebDriver Installation Verification")
st.write("This app checks if Microsoft Edge and Edge WebDriver are installed correctly.")

st.write("### Directory Contents:")
list_directory_contents("/usr/bin")
list_directory_contents("/usr/local/bin")

st.write("### Paths of Installed Packages:")
execute_command("which microsoft-edge || echo 'microsoft-edge not found'")
execute_command("microsoft-edge --version || echo 'Microsoft Edge version check failed'")
execute_command("which msedgedriver || echo 'msedgedriver not found'")
execute_command("msedgedriver --version || echo 'Edge WebDriver version check failed'")
