import os
import requests
from flask import Flask, request
import webbrowser
import urllib.parse
from dotenv import load_dotenv
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pyotp
import threading
from typing import Optional
from breeze_connect import BreezeConnect

load_dotenv()  # Load .env before accessing any environment variables

# Flask app to catch the redirect
app = Flask(__name__)
received_api_session = None
server = None

def shutdown_server():
    """Shutdown the Flask server"""
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/')
@app.route('/callback', methods=['GET', 'POST'])
def callback():
    global received_api_session
    api_session = request.args.get('apisession') or request.form.get('apisession')
    if api_session:
        received_api_session = api_session
        print(f'[INFO] Session token received: {api_session[:10]}...')
        threading.Thread(target=shutdown_server).start()
        return 'Session token received. You can close this window.'
    else:
        return 'No session token found in request.'

def start_flask_for_session():
    """Start Flask server to capture the callback"""
    global server
    server = threading.Thread(target=lambda: app.run(port=4000, debug=False, use_reloader=False))
    server.daemon = True
    server.start()
    print('[INFO] Flask server started on port 4000')
    return server

def automate_login_with_selenium(auth_url, user_id, password, totp_secret):
    """Automate login using Selenium"""
    global received_api_session
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(auth_url)
        time.sleep(1)
        
        print('[INFO] Filling login form...')
        user_id_elem = driver.find_element(By.ID, 'txtuid')
        user_id_elem.clear()
        user_id_elem.send_keys(user_id)
        time.sleep(0.2)
        
        pass_elem = driver.find_element(By.ID, 'txtPass')
        pass_elem.clear()
        pass_elem.send_keys(password)
        time.sleep(0.2)
        
        tnc_elem = driver.find_element(By.ID, 'chkssTnc')
        if not tnc_elem.is_selected():
            tnc_elem.click()
        time.sleep(0.2)
        
        print('[INFO] Submitting login form...')
        login_btn = driver.find_element(By.ID, 'btnSubmit')
        login_btn.click()
        time.sleep(1)
        
        print('[INFO] Waiting for TOTP page...')
        for _ in range(30):
            try:
                otp_inputs = driver.find_elements(By.XPATH, "//input[@tg-nm='otp']")
                if len(otp_inputs) == 6:
                    break
            except Exception:
                pass
            time.sleep(0.2)
        else:
            raise Exception('TOTP input fields not found.')
            
        print('[INFO] Entering TOTP...')
        totp = pyotp.TOTP(totp_secret).now()
        for i, digit in enumerate(totp):
            otp_inputs[i].clear()
            otp_inputs[i].send_keys(digit)
            time.sleep(0.2)
            
        print('[INFO] Submitting TOTP...')
        submit_btn = driver.find_element(By.ID, 'Button1')
        submit_btn.click()
        
        print('[INFO] Waiting for redirect and token capture...')
        time.sleep(5)
        
        current_url = driver.current_url
        print(f'[INFO] Current URL after login: {current_url}')
        
        if 'apisession' in current_url:
            print('[INFO] Token found in URL')
            # Extract token directly from URL
            token = current_url.split('apisession=')[1].split('&')[0]
            received_api_session = token
            print(f'[INFO] Token captured: {token[:10]}...')
            return token
        else:
            print('[WARN] Token not found in URL. Current page source:')
            print(driver.page_source[:500])
            
    except Exception as e:
        print(f"[ERROR] Selenium automation failed: {str(e)}")
        if driver:
            try:
                driver.save_screenshot('selenium_error.png')
                print("[INFO] Error screenshot saved as 'selenium_error.png'")
            except:
                pass
        raise
        
    finally:
        if driver:
            driver.quit()

def get_api_session(
    api_key: str,
    api_secret: str,
    user_id: Optional[str] = None,
    password: Optional[str] = None,
    totp_secret: Optional[str] = None,
    token_dir: Optional[str] = None
) -> str:
    """
    Get API session token either from stored token or by authenticating
    
    Args:
        api_key (str): Breeze API key
        api_secret (str): Breeze API secret
        user_id (str, optional): Breeze user ID for automated login
        password (str, optional): Breeze password for automated login
        totp_secret (str, optional): TOTP secret key for automated login
        token_dir (str, optional): Directory to store session token
        
    Returns:
        str: API session token
    """
    # Get token file path
    if token_dir:
        token_file = os.path.join(token_dir, "breeze_token.txt")
    else:
        token_file = os.path.join(os.path.dirname(__file__), "breeze_token.txt")

    # Try to get stored token first
    try:
        if os.path.exists(token_file):
            print("[INFO] Using stored session token.")
            with open(token_file, "r") as f:
                token = f.read().strip()
                
            # Validate token
            breeze = BreezeConnect(api_key=api_key)
            try:
                breeze.generate_session(api_secret=api_secret, session_token=token)
                return token
            except Exception as e:
                print(f"[WARN] Stored session token invalid: {str(e)}. Re-authenticating...")
    except Exception as e:
        print(f"[WARN] Error reading stored token: {str(e)}. Re-authenticating...")
    
    # Start Flask server to capture callback
    start_flask_for_session()
    auth_url = f'https://api.icicidirect.com/apiuser/login?api_key={urllib.parse.quote_plus(api_key)}&redirect_url=http://localhost:4000/callback'
    
    if user_id and password and totp_secret:
        try:
            print('[INFO] Attempting automated login with Selenium...')
            token = automate_login_with_selenium(auth_url, user_id, password, totp_secret)
            if token:
                # Store session token for future use
                _save_token(token, token_dir)
                return token
        except Exception as e:
            print(f'[ERROR] Selenium automation failed: {str(e)}')
            print('[INFO] Falling back to manual browser login...')
            print(f'[INFO] Please open this URL in your browser:\n{auth_url}')
            webbrowser.open(auth_url)
    else:
        print('[WARN] Credentials not provided for automated login.')
        print(f'[INFO] Please open this URL in your browser:\n{auth_url}')
        webbrowser.open(auth_url)
    
    # Wait for session token with timeout (only for manual login)
    timeout = time.time() + 120
    while time.time() < timeout:
        if received_api_session:
            break
        time.sleep(1)
    
    if not received_api_session:
        raise Exception('Session token not received within timeout period.')
    
    # Store session token for future use
    _save_token(received_api_session, token_dir)
    
    return received_api_session 

def _save_token(token: str, token_dir: Optional[str] = None) -> None:
    """Save session token to file"""
    if token_dir:
        token_file = os.path.join(token_dir, "breeze_token.txt")
    else:
        token_file = os.path.join(os.path.dirname(__file__), "breeze_token.txt")
        
    os.makedirs(os.path.dirname(token_file), exist_ok=True)
    with open(token_file, "w") as f:
        f.write(token) 