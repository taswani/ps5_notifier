import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import time

email_password = '' #Password for your gmail email address

def setup_email(stock, status, e_password, seller, url):
    email_config = {}

    if stock != status:
        email_config["port"] = 465  # For SSL
        email_config["smtp_server"] = "smtp.gmail.com"
        email_config["sender_email"] = ""  # Enter your gmail address
        email_config["receiver_email"] = []  # Enter receivers email addresses
        email_config["password"] = e_password
        email_config["message"] = """Subject: PS5 in stock at {}!\n\n
            PS5 {} at {}.""".format(seller, stock, url)
    
    return email_config

def send_email(stock, status, url, e_password, seller):
    '''
    stock = in_stock
    status = in_status
    url = whatever url we are currently iterating through
    e_password = email_password
    seller = place you are looking to get the PS5 from

    SMS Gateways for each Carrier

    AT&T: [number]@txt.att.net
    Sprint: [number]@messaging.sprintpcs.com or [number]@pm .sprint.com
    T-Mobile: [number]@tmomail.net
    Verizon: [number]@vtext.com
    Boost Mobile: [number]@myboostmobile.com
    Cricket: [number]@sms.mycricket.com
    Metro PCS: [number]@mymetropcs.com
    Tracfone: [number]@mmst5.tracfone.com
    U.S. Cellular: [number]@email.uscc.net
    Virgin Mobile: [number]@vmobl.com
    '''
    
    email_config = setup_email(stock, status, url, e_password, seller)

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(email_config["smtp_server"], email_config["port"], context=context) as server:
        server.login(email_config["sender_email"], email_config["password"])
        # Email
        server.sendmail(email_config["sender_email"], email_config["receiver_email"], email_config["message"])

        # Text Messaging
        msg = MIMEMultipart()
        sms_gateway_1 = '@txt.att.net' #put your att phone number before the @ symbol
        msg['From'] = email_config["sender_email"]
        msg['To'] = sms_gateway_1
        # Make sure you add a new line in the subject
        msg['Subject'] = "Subject: PS5 in stock at {}!\n".format(seller)
        # Make sure you also add new lines to your body
        body = "PS5 {} at {}.".format(stock, url)
        # and then attach that body furthermore you can also send html content.
        msg.attach(MIMEText(body, 'plain'))
        sms = msg.as_string()
        server.sendmail(email_config["sender_email"], sms_gateway_1, sms)

url_bb = 'https://www.bestbuy.com/site/playstation-5/playstation-5-packages/pcmcat1588107358954.c?irclickid=wCqWhtwKpxyLUxN0UfQwQyYMUkEymrWV1xIEXM0&irgwc=1&ref=198&loc=Narrativ&acampID=0&mpid=376373'

DRIVER_PATH = './chromedriver.exe' #Put the path to your chromedriver here, for example: C:/Users/*YourUsernameHere*/Desktop/chromedriver.exe

# START BB
def ps5_bb_notifier():
    options = Options()
    options.headless = False
    options.add_argument("--window-size=1920,1200")

    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"

    driver = webdriver.Chrome(desired_capabilities=caps, options=options, executable_path=DRIVER_PATH)
    driver.get(url_bb)
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    in_stock_bb = soup.find('button', {"class": "add-to-cart-button"}).text
    in_status_bb = 'Sold Out'
    send_email(in_stock_bb, in_status_bb, url_bb, email_password, 'best buy')
    driver.quit()


if __name__ == "__main__":
    ps5_bb_notifier()