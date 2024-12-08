from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Liste des utilisateurs
users = [
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user"
]
password = "secret_sauce"

# Initialiser le WebDriver
driver = webdriver.Chrome()

def verify_no_extra_white_space(username):
    try:
        print(f"\nINFO: Vérification du footer pour l'utilisateur : {username}")

        # Étape 1 : Charger la page de connexion
        driver.get("https://www.saucedemo.com/")
        driver.maximize_window()

        # Étape 2 : Se connecter
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login-button")))
        driver.find_element(By.ID, "user-name").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "login-button").click()

        # Vérifier la connexion
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_list")))
            print("SUCCESS: Connexion réussie.")
        except TimeoutException:
            print("ERROR: Connexion échouée.")
            return

        # Étape 3 : Vérifier la section footer
        try:
            footer = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "footer")))
            footer_bottom = footer.location['y'] + footer.size['height']
            page_height = driver.execute_script("return document.body.scrollHeight")

            # Vérifier l'absence d'espace blanc
            if footer_bottom == page_height:
                print("SUCCESS: Aucun espace blanc supplémentaire détecté sous le footer.")
            else:
                print("ERROR: Espace blanc supplémentaire détecté sous le footer.")
                print(f"Footer bottom: {footer_bottom}, Page height: {page_height}")
        except TimeoutException:
            print("ERROR: Section footer introuvable.")

    except Exception as e:
        print(f"ERROR: Une erreur s'est produite pour l'utilisateur {username}: {e}")

    finally:
        # Déconnexion
        try:
            driver.find_element(By.ID, "react-burger-menu-btn").click()
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "logout_sidebar_link"))).click()
            print(f"INFO: Déconnexion réussie pour l'utilisateur {username}.")
        except:
            print(f"WARNING: Impossible de se déconnecter pour l'utilisateur {username}.")

# Exécuter le test pour chaque utilisateur
for user in users:
    verify_no_extra_white_space(user)

# Fermer le navigateur
driver.quit()
