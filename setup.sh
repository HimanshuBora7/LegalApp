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

# Install Firefox
apt-get install -y firefox

# Install Geckodriver
GECKODRIVER_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep 'tag_name' | cut -d\" -f4)
wget -O /tmp/geckodriver.tar.gz "https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz"
tar -xzf /tmp/geckodriver.tar.gz -C /tmp
chmod +x /tmp/geckodriver
mv /tmp/geckodriver /usr/local/bin/

# Debugging: Verify Firefox and Geckodriver installation
echo "Verifying Firefox installation:"
firefox --version || echo "Firefox version check failed"

echo "Verifying Geckodriver installation:"
geckodriver --version || echo "Geckodriver version check failed"

# Debugging: List contents of the relevant directories
echo "Listing /usr/bin directory:"
ls /usr/bin
echo "Listing /usr/local/bin directory:"
ls /usr/local/bin
