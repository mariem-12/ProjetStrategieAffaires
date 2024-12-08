from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

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

def verify_footer_logo_alignment(username):
    try:
        print(f"\nINFO: Vérification de l'alignement du logo dans le footer pour l'utilisateur : {username}")

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

        # Étape 3 : Vérifier la position et l'alignement du logo
        try:
            footer = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "footer")))
            logo = footer.find_element(By.CLASS_NAME, "footer_robot")  # Assurez-vous que la classe CSS est correcte
            if logo.is_displayed():
                # Vérifier la position du logo
                logo_location = logo.location
                footer_location = footer.location
                logo_center_x = logo_location['x'] + logo.size['width'] / 2
                footer_center_x = footer_location['x'] + footer.size['width'] / 2

                if abs(logo_center_x - footer_center_x) < 5:  # Tolérance pour le centrage
                    print("SUCCESS: Le logo est correctement centré dans le footer.")
                else:
                    print(f"ERROR: Le logo n'est pas centré. Position X du logo : {logo_center_x}, Centre du footer : {footer_center_x}")
            else:
                print("ERROR: Le logo est présent dans le footer, mais n'est pas visible.")
        except NoSuchElementException:
            print("ERROR: Le logo est introuvable dans le footer.")
        except TimeoutException:
            print("ERROR: Footer introuvable sur la page.")

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
    verify_footer_logo_alignment(user)

# Fermer le navigateur
driver.quit()
