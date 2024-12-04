import os
import hashlib
import base64
import time
import requests

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def generate_code_verifier():
    # Generate a random code_verifier
    return base64.urlsafe_b64encode(os.urandom(64)).decode('utf-8').rstrip('=')


def generate_code_challenge(verifier):
    # Hash the code_verifier with SHA-256
    hashed = hashlib.sha256(verifier.encode('utf-8')).digest()
    # Base64 URL-encode the hash without padding
    return base64.urlsafe_b64encode(hashed).decode('utf-8').rstrip('=')


def get_refresh_token(code, verifier):
    res = requests.post('https://www.myefrei.fr/api-mobile/rest/public/token', data={
        'grant_type': 'authorization_code',
        'client_id': 'mobile-prod',
        'code': code,
        'code_verifier': verifier,
        'redirect_uri': 'fr.myefrei.app://'
    })
    if res.status_code != 200:
        print('Failed to get refresh token:', res.json())
        return
    print('Your refresh token is:', res.json()['refresh_token'])


def handle_network_requests(event):
    if event['params']['documentURL'].startswith('fr.myefrei.app://'):
        code = event['params']['documentURL'].split('code=')[1].split('&')[0]
        driver.quit()
        get_refresh_token(code, code_verifier)
        return {'cancel': True}


if __name__ == '__main__':
    # Generate a code_verifier
    code_verifier = generate_code_verifier()
    # Generate a corresponding code_challenge
    code_challenge = generate_code_challenge(code_verifier)

    state = os.urandom(8).hex()

    print("======== Credentials =========")
    username = input("Enter your myEfrei username: ")
    password = input("Enter your myEfrei password: ")
    print("==============================")
    print("Opening browser...")
    print("You may need to complete the CAPTCHA challenge.")

    driver = uc.Chrome(headless=False, use_subprocess=False, enable_cdp_events=True)

    driver.add_cdp_listener("Network.requestWillBeSent", handle_network_requests)

    driver.get(f'https://auth.myefrei.fr/uaa/oauth/authorize?code_challenge={code_challenge}&code_challenge_method=S256&prompt=login&redirect_uri=fr.myefrei.app%3A%2F%2F&client_id=mobile-prod&response_type=code&state={state}&scope=authorization_code+refresh_token')

    # Wait for the page to load
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'username')))

    # Fill in the username and password
    driver.find_element(By.ID, 'username').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)

    # Click the login button
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Sleep until the browser is closed
    try:
        while driver.window_handles:
            time.sleep(1)
    except:
        pass
