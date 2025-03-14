mkdir -p ~/.streamlit/

# Create credentials.toml with proper TOML format
cat <<EOL > ~/.streamlit/credentials.toml
[general]
email = ""
EOL

# Create config.toml with proper TOML format
cat <<EOL > ~/.streamlit/config.toml
[server]
headless = true
port = $PORT
enableCORS = false
EOL

apt-get update
apt-get install -y unzip curl wget

# Install Chromium browser
apt-get install -y chromium-browser

# Download and install ChromeDriver
CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget -N https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip -P /tmp
unzip /tmp/chromedriver_linux64.zip -d /tmp
chmod +x /tmp/chromedriver
mv /tmp/chromedriver /usr/local/bin/chromedriver

# Source environment variables from secrets
export CHROME_BIN=$(streamlit secrets CHROME_BIN)
export CHROME_DRIVER_PATH=$(streamlit secrets CHROME_DRIVER_PATH)

# Debug: Verify installations
echo "Verifying Chromium installation:"
$CHROME_BIN --version || echo "Chromium version check failed"

echo "Verifying ChromeDriver installation:"
$CHROME_DRIVER_PATH --version || echo "ChromeDriver version check failed"

# Debugging: List contents of relevant directories
echo "Listing /usr/bin:"
ls /usr/bin
echo "Listing /usr/local/bin:"
ls /usr/local/bin
