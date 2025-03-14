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
apt-get install -y chromium-browser
apt-get install -y chromium-chromedriver

# Debugging: List contents of the relevant directories
echo "Listing /usr/bin directory:"
ls /usr/bin
echo "Listing /usr/lib/chromium-browser directory:"
ls /usr/lib/chromium-browser

# Create symlinks for Chrome and ChromeDriver
ln -s /usr/bin/chromium-browser /usr/bin/google-chrome
ln -s /usr/lib/chromium-browser/chromedriver /usr/local/bin/chromedriver
