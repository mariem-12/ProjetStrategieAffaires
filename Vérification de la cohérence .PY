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

def verify_footer_consistency(username):
    try:
        print(f"\nINFO: Vérification de la section footer pour l'utilisateur : {username}")

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

        # Étape 3 : Capturer le footer de la page d'inventaire
        try:
            inventory_footer = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "footer")))
            inventory_footer_html = inventory_footer.get_attribute("innerHTML")
            print("INFO: Footer capturé sur la page d'inventaire.")
        except TimeoutException:
            print("ERROR: Footer introuvable sur la page d'inventaire.")
            return

        # Étape 4 : Vérifier la cohérence du footer sur d'autres pages
        pages = [
            "cart.html",
            "checkout-step-one.html",
            "checkout-step-two.html",
            "checkout-complete.html"
        ]
        for page in pages:
            driver.get(f"https://www.saucedemo.com/{page}")
            try:
                footer = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "footer")))
                footer_html = footer.get_attribute("innerHTML")
                if footer_html == inventory_footer_html:
                    print(f"SUCCESS: Le footer sur {page} est cohérent.")
                else:
                    print(f"ERROR: Le footer sur {page} n'est pas cohérent avec la page d'inventaire.")
            except TimeoutException:
                print(f"ERROR: Footer introuvable sur {page}.")

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
    verify_footer_consistency(user)

# Fermer le navigateur
driver.quit()
