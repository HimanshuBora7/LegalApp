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

# Check available Chromium packages
echo "Checking available Chromium packages:"
apt-cache search chromium

# Install Chromium and ChromeDriver
echo "Installing chromium-browser and chromium-chromedriver:"
apt-get install -y chromium-browser chromium-chromedriver

# Debugging: Check paths of installed packages
echo "Paths of installed packages:"
which chromium-browser
which chromedriver

# Set environment variable for Chrome binary
echo "Setting CHROME_BIN environment variable:"
echo "export CHROME_BIN=$(which chromium-browser)" >> ~/.bashrc
source ~/.bashrc

# Debugging: List contents of the relevant directories
echo "Listing /usr/bin directory:"
ls /usr/bin
echo "Listing /usr/local/bin directory:"
ls /usr/local/bin
