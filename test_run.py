from selenium import webdriver

try:
    # Set up the WebDriver
    driver = webdriver.Chrome()

    # Open a website to test
    driver.get("https://www.google.com")

    print("ChromeDriver is working correctly!")

    # Close the browser
    driver.quit()

except Exception as e:
    print(f"Something went wrong: {e}")
