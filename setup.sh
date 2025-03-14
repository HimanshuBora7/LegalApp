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

# Install Chromium
echo "Installing Chromium..."
apt-get install -y chromium-browser

# Add Chromium to the PATH
echo "Adding Chromium to the PATH..."
ln -s /usr/bin/chromium-browser /usr/local/bin/chromium-browser

# Verify Chromium installation
echo "Verifying Chromium installation:"
/usr/local/bin/chromium-browser --version || echo "chromium-browser version check failed"

# Install ChromeDriver using chromedriver_autoinstaller
echo "Installing ChromeDriver..."
pip install chromedriver-autoinstaller
python -c "import chromedriver_autoinstaller; chromedriver_autoinstaller.install()"

# Debugging: List contents of the relevant directories
echo "Listing /usr/bin directory:"
ls /usr/bin
echo "Listing /usr/local/bin directory:"
ls /usr/local/bin

