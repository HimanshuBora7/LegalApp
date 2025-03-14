mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
" > ~/.streamlit/config.toml

apt-get update
apt-get install -y unzip curl

# Install Chromium and ChromeDriver
apt-get install -y chromium-browser chromium-chromedriver

# Set environment variable for Chrome binary
echo "export CHROME_BIN=/usr/bin/chromium-browser" >> ~/.bashrc
source ~/.bashrc

# Debugging: List contents of the relevant directories and paths of installed packages
echo "Listing /usr/bin directory:"
ls /usr/bin
echo "Listing /usr/local/bin directory:"
ls /usr/local/bin
