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

# Download and install Microsoft Edge
echo "Downloading Microsoft Edge..."
wget -O /tmp/microsoft-edge.deb https://packages.microsoft.com/repos/edge/pool/main/m/microsoft-edge-stable/microsoft-edge-stable_91.0.864.48-1_amd64.deb
apt-get install -y /tmp/microsoft-edge.deb

# Download and install Edge WebDriver
echo "Downloading Edge WebDriver..."
EDGE_VERSION=$(microsoft-edge --version | grep -oP '\d+\.\d+\.\d+\.\d+')
wget -O /tmp/edgedriver.zip "https://msedgedriver.azureedge.net/$EDGE_VERSION/edgedriver_linux64.zip"
unzip /tmp/edgedriver.zip -d /tmp
chmod +x /tmp/msedgedriver
mv /tmp/msedgedriver /usr/local/bin/

# Debugging: Verify Microsoft Edge and Edge WebDriver installation
echo "Verifying Microsoft Edge installation:"
microsoft-edge --version || echo "Microsoft Edge version check failed"

echo "Verifying Edge WebDriver installation:"
msedgedriver --version || echo "Edge WebDriver version check failed"

# Debugging: List contents of the relevant directories
echo "Listing /usr/bin directory:"
ls /usr/bin
echo "Listing /usr/local/bin directory:"
ls /usr/local/bin
