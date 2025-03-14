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

# Install Chromium
apt-get install -y chromium-browser

# Verify Chromium installation
echo "Verifying Chromium installation:"
which chromium-browser
chromium-browser --version

# Download and install ChromeDriver using chromedriver_autoinstaller
pip install chromedriver-autoinstaller
python -c "import chromedriver_autoinstaller; chromedriver_autoinstaller.install()"

# Set environment variable for Chrome binary
echo "export CHROME_BIN=/usr/bin/chromium-browser" >> ~/.bashrc
source ~/.bashrc

# Debugging: List contents of the relevant directories
echo "Listing /usr/bin directory:"
ls /usr/bin
echo "Listing /usr/local/bin directory:"
ls /usr/local/bin
