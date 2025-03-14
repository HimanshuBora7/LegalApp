import streamlit as st
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

st.title("Chromium Installation Verification")
st.write("This app checks if Chromium is installed correctly.")

st.write("### Directory Contents:")
list_directory_contents("/usr/bin")
list_directory_contents("/usr/local/bin")

st.write("### Paths of Installed Packages:")
execute_command("which chromium-browser || echo 'chromium-browser not found'")
execute_command("chromium-browser --version || echo 'chromium-browser version check failed'")
