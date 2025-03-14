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
apt-get install -y unzip curl wget

# Download and install Chromium
echo "Downloading Chromium..."
wget -O /tmp/chromium.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
echo "Installing Chromium..."
apt-get install -y /tmp/chromium.deb

# Download and install ChromeDriver
echo "Downloading ChromeDriver..."
CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+\.\d+')
wget -N https://chromedriver.storage.googleapis.com/${CHROME_VERSION%%.*}/chromedriver_linux64.zip -P /tmp
unzip /tmp/chromedriver_linux64.zip -d /tmp
chmod +x /tmp/chromedriver
mv /tmp/chromedriver /usr/local/bin/chromedriver

# Set environment variable for Chrome binary
echo "export CHROME_BIN=/usr/bin/google-chrome" >> ~/.bashrc
source ~/.bashrc

# Debugging: List contents of the relevant directories and paths of installed packages
echo "Listing /usr/bin directory:"
ls /usr/bin
echo "Listing /usr/local/bin directory:"
ls /usr/local/bin
echo "Listing /opt/google/chrome directory (if it exists):"
ls /opt/google/chrome || echo "/opt/google/chrome not found"
