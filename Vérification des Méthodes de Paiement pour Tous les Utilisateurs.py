from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Liste des utilisateurs de test
users = [
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
    "visual_user"
]
password = "secret_sauce"
# Initialiser le WebDriver
driver = webdriver.Chrome()

def verify_payment_methods(username):
    try:
        print(f"\nINFO: Test en cours pour l'utilisateur : {username}")

        # Étape 1 : Charger la page de connexion
        driver.get("https://www.saucedemo.com/")
        driver.maximize_window()

        # Étape 2 : Se connecter
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login-button")))
        driver.find_element(By.ID, "user-name").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "login-button").click()

        # Vérifier si la connexion est réussie
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_list")))
            print("SUCCESS: Connexion réussie pour l'utilisateur.")
        except TimeoutException:
            raise AssertionError("ERROR: Connexion échouée.")

        # Étape 3 : Ajouter un produit au panier
        product_add_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn_inventory"))
        )
        product_add_button.click()
        print("INFO: Produit ajouté au panier.")

        # Étape 4 : Aller au panier
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

        # Étape 5 : Cliquer sur le bouton de paiement
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "checkout"))).click()

        # Étape 6 : Remplir les informations de paiement
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "first-name")))
        driver.find_element(By.ID, "first-name").send_keys("John")
        driver.find_element(By.ID, "last-name").send_keys("Doe")
        driver.find_element(By.ID, "postal-code").send_keys("12345")
        driver.find_element(By.ID, "continue").click()

        # Étape 7 : Vérifier les méthodes de paiement disponibles
        print("INFO: Vérification des méthodes de paiement...")
        payment_methods = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "payment_method"))  # Remplacez par le sélecteur approprié
        )
        assert len(payment_methods) > 0, "ERROR: Aucune méthode de paiement disponible."
        print(f"SUCCESS: {len(payment_methods)} méthode(s) de paiement disponible(s) pour l'utilisateur.")

    except NoSuchElementException as e:
        print(f"ERROR: Élément manquant pour l'utilisateur {username}: {e}")
    except AssertionError as e:
        print(f"ERROR: Problème détecté pour l'utilisateur {username}: {e}")
    except Exception as e:
        print(f"ERROR: Une erreur inattendue s'est produite pour l'utilisateur {username}: {e}")
    finally:
        # Déconnexion
        try:
            driver.find_element(By.ID, "react-burger-menu-btn").click()
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "logout_sidebar_link"))).click()
            print(f"INFO: Déconnexion réussie pour l'utilisateur {username}.")
        except:
            print(f"WARNING: Impossible de se déconnecter pour l'utilisateur {username}.")

# Tester chaque utilisateur
for user in users:
    verify_payment_methods(user)

# Fermer le navigateur
driver.quit()
