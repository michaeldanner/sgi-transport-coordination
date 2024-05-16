import time
from selenium import webdriver
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By

total_pages = 2

driver = webdriver.Chrome()
driver.maximize_window()
# Load the Dash app
driver.get('http://localhost:8050')  # Adjust to your Dash app URL
time.sleep(5)  # Wait for the page to load


# Take a screenshot
element = driver.find_element(By.CLASS_NAME, 'table-card')  # Use the ID of your card component
element.screenshot('screenshot.png')

# Convert screenshot to PDF
img = Image.open('screenshot.png')
img_width, img_height = img.size

# Create a PDF with the same dimension as the image
c = canvas.Canvas('output.pdf', pagesize=(img_width, img_height))

for i in range(total_pages):
    element = driver.find_element(By.ID, f'id+{i}')  # Use the ID of your card component
    element.screenshot(f'screenshot{i}.png')

    # Convert screenshot to PDF
    c.drawImage(f'screenshot{i}.png', 0, 0, width=img_width, height=img_height)
    c.showPage()
c.save()

# Clean up
driver.quit()
