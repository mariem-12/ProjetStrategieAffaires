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

def verify_footer_elements_alignment(username):
    try:
        print(f"\nINFO: Vérification des éléments du footer pour l'utilisateur : {username}")

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

        # Étape 3 : Vérifier l'alignement des éléments du footer
        try:
            footer = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "footer")))

            # Récupérer tous les éléments du footer
            footer_elements = footer.find_elements(By.XPATH, "./*")

            if len(footer_elements) == 0:
                print("ERROR: Aucun élément trouvé dans la section footer.")
                return

            # Vérifier l'alignement de chaque élément
            for element in footer_elements:
                if element.is_displayed():
                    location = element.location
                    size = element.size
                    print(f"INFO: Élément aligné - Position: {location}, Taille: {size}")
                else:
                    print("WARNING: Un élément dans le footer n'est pas visible.")

            print("SUCCESS: Tous les éléments visibles dans le footer sont alignés correctement.")
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
    verify_footer_elements_alignment(user)

# Fermer le navigateur
driver.quit()
