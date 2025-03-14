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

st.title("Firefox and Geckodriver Installation Verification")
st.write("This app checks if Firefox and Geckodriver are installed correctly.")

st.write("### Directory Contents:")
list_directory_contents("/opt/firefox")
list_directory_contents("/usr/local/bin")

st.write("### Paths of Installed Packages:")
execute_command("/usr/local/bin/firefox --version || echo 'Firefox version check failed'")
execute_command("/usr/local/bin/geckodriver --version || echo 'Geckodriver version check failed'")
