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

st.title("Portable Chromium Installation Verification")
st.write("This app checks if portable Chromium is installed correctly.")

st.write("### Directory Contents:")
list_directory_contents("/tmp/chrome-linux")

st.write("### Paths of Installed Packages:")
execute_command("which /tmp/chrome-linux/chrome || echo '/tmp/chrome-linux/chrome not found'")
execute_command("/tmp/chrome-linux/chrome --version || echo 'Portable Chromium version check failed'")
