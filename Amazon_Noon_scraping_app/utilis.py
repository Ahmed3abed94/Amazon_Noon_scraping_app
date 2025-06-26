from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def init_driver():
    opts = Options()
    # Uncomment this line if you want to run Chrome in headless mode (no browser window)
    opts.add_argument("--headless")  

    opts.add_argument("--no-sandbox")  # Recommended for some Linux environments
    opts.add_argument("--disable-dev-shm-usage")  # Avoids shared memory issues in Docker/Linux
    opts.add_experimental_option("detach", True)  # Keeps browser open after script ends

    # Preferences to block loading images, CSS, and plugins for faster scraping
    prefs = {
        "profile.managed_default_content_settings.images": 2,      # Block images
        "profile.managed_default_content_settings.stylesheets": 2,  # Block CSS
        "profile.managed_default_content_settings.plugins": 2,      # Block plugins
        "profile.managed_default_content_settings.javascript": 1,   # Enable JavaScript (set 0 to disable, but site may break)
        "profile.managed_default_content_settings.popups": 2        # Block popups
    }
    opts.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=opts)
    driver.minimize_window()
    return driver
