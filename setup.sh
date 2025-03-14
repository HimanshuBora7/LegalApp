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
echo "Installing Chromium..."
apt-get install -y chromium-browser

# Debug: Ensure Chromium is installed
if [ -f /usr/bin/chromium-browser ]; then
    echo "Chromium installed successfully"
else
    echo "Chromium installation failed"
    exit 1
fi

# Symlink Chromium to /usr/local/bin
ln -s /usr/bin/chromium-browser /usr/local/bin/chromium-browser

# Install ChromeDriver using chromedriver_autoinstaller
echo "Installing ChromeDriver..."
pip install chromedriver-autoinstaller
python -c "import chromedriver_autoinstaller; chromedriver_autoinstaller.install()"

# Debug: List contents of directories
echo "Listing /usr/bin:"
ls /usr/bin
echo "Listing /usr/local/bin:"
ls /usr/local/bin
echo "Listing /opt/google/chrome:"
ls /opt/google/chrome

# Verify installations
/usr/local/bin/chromium-browser --version || echo "Chromium version check failed"
/usr/local/bin/chromedriver --version || echo "ChromeDriver version check failed"
