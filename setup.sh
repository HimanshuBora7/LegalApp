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

# Download and extract portable Chromium
echo "Downloading portable Chromium..."
wget -O /tmp/chrome-linux.zip https://commondatastorage.googleapis.com/chromium-browser-snapshots/Linux_x64/706915/chrome-linux.zip
if [ $? -ne 0 ]; then
    echo "Failed to download Chromium"
    exit 1
fi

echo "Extracting portable Chromium..."
unzip /tmp/chrome-linux.zip -d /tmp
if [ $? -ne 0 ]; then
    echo "Failed to extract Chromium"
    exit 1
fi

chmod +x /tmp/chrome-linux/chrome

# Set environment variable for Chrome binary
echo "export CHROME_BIN=/tmp/chrome-linux/chrome" >> ~/.bashrc
source ~/.bashrc

# Debugging: Verify Chromium installation
echo "Verifying Chromium installation:"
/tmp/chrome-linux/chrome --version || echo "Portable Chromium version check failed"

# Debugging: List contents of the relevant directories
echo "Listing /tmp/chrome-linux directory:"
ls /tmp/chrome-linux
