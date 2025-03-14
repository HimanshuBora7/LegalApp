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
apt-get install -y unzip curl wget gnupg

# Add Chromium repository and install Chromium
curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list'
apt-get update
apt-get install -y google-chrome-stable

# Verify installation of Chromium
echo "Verifying Chromium installation:"
which google-chrome || echo "google-chrome not found"
google-chrome --version || echo "google-chrome version check failed"

# Debugging: List contents of the relevant directories
echo "Listing /usr/bin directory:"
ls /usr/bin
echo "Listing /usr/local/bin directory:"
ls /usr/local/bin
