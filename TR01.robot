*** Settings ***
Library           SeleniumLibrary
Suite Setup       Open Browser To Login Page
Suite Teardown    Close Browser

*** Variables ***
${LOGIN_URL}      https://www.saucedemo.com
${BROWSER}        Chrome
${USERNAME}       standard_user
${PASSWORD}       secret_sauce

*** Test Cases ***
Test Connexion Avec Identifiants Valides
    [Documentation]  Vérifie qu'un utilisateur avec des identifiants valides peut se connecter.
    Input Username
    Input Password
    Click Login Button
    Verify Login Successful

*** Keywords ***
Open Browser To Login Page
    Open Browser    ${LOGIN_URL}    ${BROWSER}
    Maximize Browser Window

Input Username
    Input Text      id:user-name    ${USERNAME}

Input Password
    Input Text      id:password     ${PASSWORD}

Click Login Button
    Click Button    id:login-button

Verify Login Successful
    Wait Until Page Contains Element    id:inventory_container
    Element Should Be Visible           id:inventory_container
