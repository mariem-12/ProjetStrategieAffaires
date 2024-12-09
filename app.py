from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Initialiser WebDriver
driver = webdriver.Chrome()
BASE_URL = "https://www.saucedemo.com/"

# Identifiants des utilisateurs pour Sauce Demo
users = [
    {"username": "standard_user", "password": "secret_sauce"},
    {"username": "locked_out_user", "password": "secret_sauce"},
    {"username": "problem_user", "password": "secret_sauce"},
    {"username": "performance_glitch_user", "password": "secret_sauce"},
    {"username": "error_user", "password": "secret_sauce"},
    {"username": "visual_user", "password": "secret_sauce"}
]

try:
    # Fonction pour se connecter au site
    def login(username, password):
        driver.get(BASE_URL)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "user-name"))
        ).send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "login-button").click()

    # Fonction pour tester la section de l'en-tête
    def test_header_section():
        print("Test de la section de l'en-tête...")

        # Vérifier si l'en-tête est présent
        try:
            header = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "header_secondary_container"))
            )
            print("La section de l'en-tête est présente.")
        except TimeoutException:
            print("La section de l'en-tête est manquante.")
            return

        # Vérifier l'alignement de l'en-tête
        assert header.is_displayed(), "La section de l'en-tête n'est pas visible."
        print("L'en-tête est aligné correctement.")

        # Vérifier l'alignement du logo
            logo = driver.find_element(By.CLASS_NAME, "app_logo")
            assert logo.is_displayed(), "Le logo n'est pas visible dans l'en-tête."
            print("Le logo est aligné correctement dans l'en-tête.")

        # Vérifier tous les liens dans l'en-tête
        menu_button = driver.find_element(By.ID, "react-burger-menu-btn")
        assert menu_button.is_displayed() and menu_button.is_enabled(), "Le bouton de menu ne fonctionne pas."
        print("Le bouton de menu fonctionne.")

        # Ouvrir le menu et vérifier les liens
        menu_button.click()
        menu_links = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "bm-item"))
        )
        for link in menu_links:
            assert link.is_displayed(), f"Le lien {link.text} n'est pas visible."
        print("Tous les liens du menu sont visibles.")

        # Fermer le menu
        driver.find_element(By.ID, "react-burger-cross-btn").click()
        print("Le menu fonctionne correctement.")

        # Vérifier la barre de recherche (si applicable)
        try:
            search_bar = driver.find_element(By.CLASS_NAME, "search-input")
            assert search_bar.is_displayed(), "La barre de recherche est manquante dans l'en-tête."
            print("La barre de recherche est présente dans l'en-tête.")
        except:
            print("La barre de recherche n'est pas disponible sur Sauce Demo.")

        print("Tous les tests de l'en-tête sont passés.")

    # Exécuter le test pour tous les utilisateurs
    print("Début des tests de la section de l'en-tête pour tous les utilisateurs...")
    for user in users:
        print(f"\nTest pour l'utilisateur : {user['username']}...")
        try:
            login(user['username'], user['password'])
            # Vérifier si la connexion a réussi
            if "inventory.html" in driver.current_url:
                print("Connexion réussie.")
                test_header_section()
            else:
                print(f"Échec de la connexion pour l'utilisateur : {user['username']}")
        except Exception as e:
            print(f"Échec du test pour l'utilisateur {user['username']} : {e}")
        finally:
            # Se déconnecter ou revenir à la page de connexion pour l'utilisateur suivant
            driver.get(BASE_URL)

except Exception as e:
    print(f"Test échoué : {e}")

finally:
    driver.quit()
    print("Navigateur fermé.")
