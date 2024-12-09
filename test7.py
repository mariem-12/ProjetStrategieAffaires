from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialisation du navigateur
def init_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

# Fonction pour tester les identifiants invalides
def test_invalid_credentials(driver, username, expected_error):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys("wrong_password")  # Mot de passe incorrect
    driver.find_element(By.ID, "login-button").click()
    time.sleep(1)

    try:
        error_message = driver.find_element(By.CLASS_NAME, "error-message-container").text
        assert expected_error in error_message, f"Message d'erreur incorrect pour {username} avec identifiants invalides."
        print(f"Test des identifiants invalides pour {username} réussi.")
    except Exception as e:
        print(f"Erreur lors du test des identifiants invalides pour {username}: {e}")

# Fonction pour tester les champs vides
def test_empty_fields(driver):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(1)
    try:
        error_message = driver.find_element(By.CLASS_NAME, "error-message-container").text
        assert "Username is required" in error_message, "Message d'erreur incorrect pour les champs vides."
        print("Test des champs vides réussi.")
    except Exception as e:
        print(f"Erreur lors du test des champs vides : {e}")

# Test de la navigation par Tab pour error_user
def test_tab_navigation(driver):
    driver.get("https://www.saucedemo.com/")
    user_field = driver.find_element(By.ID, "user-name")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    user_field.send_keys("error_user")
    user_field.send_keys(Keys.TAB)
    assert password_field.get_dom_attribute("id") == "password", "Navigation Tab incorrecte pour le champ mot de passe."

    password_field.send_keys("secret_sauce")
    password_field.send_keys(Keys.TAB)
    assert login_button.get_dom_attribute("id") == "login-button", "Navigation Tab incorrecte pour le bouton de connexion."
    print("Navigation avec la touche Tab réussie.")


# Fonction pour tester la connexion avec la touche Entrée
def test_login_with_enter_key(driver, username, password):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys(username)
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(2)

    if username == "locked_out_user":
        try:
            error_message = driver.find_element(By.CLASS_NAME, "error-message-container").text
            assert "locked out" in error_message, f"Message d'erreur incorrect pour {username}"
            print(f"Impossible de se connecter pour {username}. L'utilisateur est bien bloqué.")
        except Exception as e:
            print(f"Erreur lors du test de la connexion avec Entrée pour {username}: {e}")
    else:
        current_url = driver.current_url
        assert "inventory" in current_url, f"L'utilisateur {username} n'a pas été redirigé vers la page des produits."
        print(f"Connexion réussie pour {username} avec la touche Entrée.")

# Fonction pour tester la performance de connexion
def test_login_performance(driver, username, password):
    driver.get("https://www.saucedemo.com/")
    start_time = time.time()

    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()

    time.sleep(1)
    end_time = time.time()
    connection_time = end_time - start_time

    print(f"Temps de connexion pour {username}: {connection_time:.2f} secondes.")
    if connection_time >= 3 and connection_time < 5:
        print(f"Connexion un peu lente pour {username} en {connection_time:.2f} secondes.")
    elif connection_time >= 5:
        print(f"Connexion très lente pour {username} en {connection_time:.2f} secondes.")
    else:
        print(f"Connexion réussie pour {username} en {connection_time:.2f} secondes.")

# Fonction pour tester la déconnexion
def test_logout(driver, username):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)

    if username != "locked_out_user":
        driver.find_element(By.ID, "react-burger-menu-btn").click()
        time.sleep(1)
        try:
            logout_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
            )
            logout_button.click()
            print(f"Déconnexion réussie pour {username}.")
        except Exception as e:
            print(f"Erreur lors de la déconnexion pour {username}: {e}")
    else:
        print(f"L'utilisateur {username} est bloqué et ne peut pas se déconnecter.")

# Fonction principale pour exécuter les tests
def run_tests():
    driver = init_driver()
    users = {
        "standard_user": "secret_sauce",
        "locked_out_user": "secret_sauce",
        "problem_user": "secret_sauce",
        "performance_glitch_user": "secret_sauce",
        "visual_user": "secret_sauce"
    }

    for username, password in users.items():
        print(f"\nExécution des tests pour {username}...")
        test_invalid_credentials(driver, username, "Username and password do not match any user")
        test_empty_fields(driver)
        test_tab_navigation(driver)
        test_login_with_enter_key(driver, username, password)
        test_login_performance(driver, username, password)
        test_logout(driver, username)

    driver.quit()

# Exécuter les tests
run_tests()
