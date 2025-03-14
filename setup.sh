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

# Install Chromium Browser Snap
apt-get install -y software-properties-common
add-apt-repository -y ppa:canonical-chromium-builds/stage
apt-get update
apt-get install -y chromium-browser

# Verify installation of Chromium
echo "Verifying Chromium installation:"
which chromium-browser || echo "chromium-browser not found"
chromium-browser --version || echo "chromium-browser version check failed"

# Debugging: List contents of the relevant directories
echo "Listing /usr/bin directory:"
ls /usr/bin
echo "Listing /usr/local/bin directory:"
ls /usr/local/bin
