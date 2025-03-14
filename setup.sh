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

# Install Chromium
apt-get install -y chromium-browser

# Download and install ChromeDriver
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get install -y ./google-chrome-stable_current_amd64.deb

CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+\.\d+')
wget -N https://chromedriver.storage.googleapis.com/$CHROME_VERSION/chromedriver_linux64.zip -P /tmp
unzip /tmp/chromedriver_linux64.zip -d /tmp
chmod +x /tmp/chromedriver
mv /tmp/chromedriver /usr/local/bin/chromedriver

# Set environment variable for Chrome binary
echo "export CHROME_BIN=/opt/google/chrome/google-chrome" >> ~/.bashrc
source ~/.bashrc

# Debugging: List contents of the relevant directories and paths of installed packages
echo "Listing /usr/bin directory:"
ls /usr/bin
echo "Listing /usr/local/bin directory:"
ls /usr/local/bin
echo "Listing /opt/google/chrome directory:"
ls /opt/google/chrome
echo "Checking paths of installed packages:"
which chromium-browser
which chromedriver
which google-chrome
