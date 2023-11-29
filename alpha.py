from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_latest_video_link(channel_link):
    try:
        # Initialize Selenium WebDriver for Firefox (make sure you have the appropriate driver installed)
        driver = webdriver.Firefox()

        # Load the channel page
        driver.get(channel_link)

        # Wait for the page to load and the latest video link to become clickable
        latest_video_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a#video-title'))
        )

        # Get the link to the latest video
        latest_video_link_url = latest_video_link.get_attribute('href')

        return latest_video_link_url
    except Exception as e:
        print(f"Error al obtener el enlace del último video: {str(e)}")
        return None
    finally:
        # Close the browser window
        if driver:
            driver.quit()

# Example usage:
channel_link = 'https://www.youtube.com/@melvinthinks'
latest_video_link = get_latest_video_link(channel_link)

if latest_video_link:
    print(f"Enlace al último video: {latest_video_link}")
else:
    print("No se pudo obtener el enlace del último video.")
