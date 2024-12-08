from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration du service ChromeDriver
service = Service('./chromedriver.exe') 
driver = webdriver.Chrome(service=service)

try:
    # Accéder au site
    driver.get("https://www.saucedemo.com")

    # Attendre que le champ username soit visible
    username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "user-name"))
    )

    # Trouver le champ password
    password = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
    )

    # Trouver le bouton login
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "login-button"))
    )

    # Remplir les informations
    username.send_keys("standard_user")
    password.send_keys("secret_sauce")
    login_button.click()

    # Vérifier que la page suivante charge correctement
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "inventory_container"))
    )

    print("Connexion réussie !")
finally:
    driver.quit()
