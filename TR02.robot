*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}      https://www.saucedemo.com
${INVALID_USERNAME}    invalid_user
${INVALID_PASSWORD}    invalid_password

*** Test Cases ***
Test de Connexion avec Identifiants Invalides
    [Documentation]    Ce test tente de se connecter avec des identifiants invalides
    [Tags]    Regression
    Ouvrir le Navigateur
    Tenter de se connecter avec des identifiants invalides
    Vérifier le message d'erreur
    Fermer le Navigateur

*** Keywords ***
Ouvrir le Navigateur
    Open Browser    ${URL}    Chrome
    Maximize Browser Window

Tenter de se connecter avec des identifiants invalides
    Input Text    id=user-name    ${INVALID_USERNAME}
    Input Text    id=password    ${INVALID_PASSWORD}
    Click Button    id=login-button

Vérifier le message d'erreur
    ${error_message}=    Get Text    css=.error-message-container
    Should Contain    ${error_message}    Epic sadface: login et mot de passe invalides

Fermer le Navigateur
    Close Browser
