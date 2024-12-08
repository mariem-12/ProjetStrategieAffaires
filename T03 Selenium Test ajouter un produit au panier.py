from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuration du service ChromeDriver
service = Service('./chromedriver.exe')  # Remplacez par le chemin correct de votre ChromeDriver
driver = webdriver.Chrome(service=service)

try:
    # Étape 1 : Accéder au site
    driver.get("https://www.saucedemo.com")

    # Étape 2 : Se connecter
    # Attendre que le champ username soit visible
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user-name")))
    username = driver.find_element(By.ID, "user-name")
    password = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    # Entrer les identifiants
    username.send_keys("standard_user")
    password.send_keys("secret_sauce")
    login_button.click()

    # Attendre que la page suivante soit chargée
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "inventory_container")))

    # Étape 3 : Ajouter un produit au panier
    product_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
    )
    product_button.click()

    # Étape 4 : Accéder au panier
    cart_button = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    cart_button.click()

    # Attendre que la page du panier soit chargée
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cart_item")))

    # Étape 5 : Vérifier que le produit est ajouté
    product_in_cart = driver.find_element(By.CLASS_NAME, "inventory_item_name")
    assert "Sauce Labs Backpack" in product_in_cart.text, "Le produit n'a pas été ajouté au panier."

    print("Test réussi : Le produit a été ajouté au panier.")
finally:
    # Fermer le navigateur
    driver.quit()
