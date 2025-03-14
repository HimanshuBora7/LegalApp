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

# Update package list and install dependencies
apt-get update
apt-get install -y unzip curl wget

# Download and install Firefox
echo "Downloading Firefox..."
wget -O /tmp/firefox.tar.bz2 https://download.mozilla.org/?product=firefox-latest&os=linux64&lang=en-US
tar -xjf /tmp/firefox.tar.bz2 -C /tmp
mv /tmp/firefox /opt/firefox

# Create a symlink to Firefox
ln -s /opt/firefox/firefox /usr/local/bin/firefox

# Download and install Geckodriver
echo "Downloading Geckodriver..."
GECKODRIVER_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep 'tag_name' | cut -d\" -f4)
wget -O /tmp/geckodriver.tar.gz "https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz"
tar -xzf /tmp/geckodriver.tar.gz -C /tmp
chmod +x /tmp/geckodriver
mv /tmp/geckodriver /usr/local/bin/

# Debugging: Verify Firefox and Geckodriver installation
echo "Verifying Firefox installation:"
/usr/local/bin/firefox --version || echo "Firefox version check failed"

echo "Verifying Geckodriver installation:"
/usr/local/bin/geckodriver --version || echo "Geckodriver version check failed"

# Debugging: List contents of the relevant directories
echo "Listing /opt/firefox directory:"
ls /opt/firefox
echo "Listing /usr/local/bin directory:"
ls /usr/local/bin
