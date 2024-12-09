import imaplib
import email
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

# Détails de l'email pour la vérification
EMAIL_USER = "votre_email@example.com"  # Remplacez par votre adresse email
EMAIL_PASS = "votre_mot_de_passe"       # Remplacez par le mot de passe de votre boîte email
EMAIL_SERVER = "imap.gmail.com"         # Remplacez par votre serveur IMAP (ex. : Gmail, Outlook)

# Initialiser le WebDriver
driver = webdriver.Chrome()

def place_order(username):
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

        # Étape 6 : Remplir les informations personnelles
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "first-name")))
        driver.find_element(By.ID, "first-name").send_keys("John")
        driver.find_element(By.ID, "last-name").send_keys("Doe")
        driver.find_element(By.ID, "postal-code").send_keys("12345")
        driver.find_element(By.ID, "continue").click()

        # Étape 7 : Finaliser l'achat
        print("INFO: Finalisation de la commande...")
        driver.find_element(By.ID, "finish").click()
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "complete-header")))
        print("SUCCESS: Commande finalisée avec succès.")

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

def check_email_for_order():
    try:
        print("INFO: Vérification des emails pour la confirmation de commande...")
        
        # Connexion au serveur email
        mail = imaplib.IMAP4_SSL(EMAIL_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        # Rechercher les emails contenant un sujet spécifique
        result, data = mail.search(None, '(SUBJECT "Order Confirmation")')
        if data[0]:
            print("SUCCESS: Email de confirmation trouvé.")
        else:
            print("ERROR: Aucun email de confirmation trouvé.")
        
        mail.logout()

    except Exception as e:
        print(f"ERROR: Une erreur s'est produite lors de la vérification des emails : {e}")

# Tester la commande
for user in users:
    place_order(user)

# Vérifier les emails
check_email_for_order()

# Fermer le navigateur
driver.quit()
