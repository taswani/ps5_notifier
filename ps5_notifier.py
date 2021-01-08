import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import time

username = '' #Costco username
password = '' #Costco password
email_password = '' #Password for your gmail email address

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
    if stock != status:
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = ""  # Enter your gmail address
        receiver_email = []  # Enter receivers email addresses
        password = e_password
        message = """Subject: PS5 in stock at {}!\n\n

    PS5 {} at {}.""".format(seller, stock, url)

        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            # Email
            server.sendmail(sender_email, receiver_email, message)

            # Text Messaging
            msg = MIMEMultipart()
            sms_gateway_1 = '@txt.att.net' #put your att phone number before the @ symbol
            msg['From'] = sender_email
            msg['To'] = sms_gateway_1
            # Make sure you add a new line in the subject
            msg['Subject'] = "Subject: PS5 in stock at {}!\n".format(seller)
            # Make sure you also add new lines to your body
            body = "PS5 {} at {}.".format(stock, url)
            # and then attach that body furthermore you can also send html content.
            msg.attach(MIMEText(body, 'plain'))
            sms = msg.as_string()
            server.sendmail(sender_email, sms_gateway_1, sms)


url_target = 'https://www.target.com/p/playstation-5-console/-/A-81114595?clkid=de251659N4bdd11eb8a0142010a246cc4&lnm=81938&afid=Future%20PLC.&ref=tgt_adv_xasd0002'
url_bb = 'https://www.bestbuy.com/site/playstation-5/playstation-5-packages/pcmcat1588107358954.c?irclickid=wCqWhtwKpxyLUxN0UfQwQyYMUkEymrWV1xIEXM0&irgwc=1&ref=198&loc=Narrativ&acampID=0&mpid=376373'
url_costco_login = 'https://www.costco.com/LogonForm'
url_costco = 'https://www.costco.com/sony-playstation-5-gaming-console-bundle.product.100691489.html'
url_sony = 'https://direct.playstation.com/en-us/consoles/console/playstation5-console.3005816'

DRIVER_PATH = '' #Put the path to your chromedriver here, for example: C:/Users/*YourUsernameHere*/Desktop/chromedriver.exe

# There is definitely potential to refactor all the code below, but I'm lazy as all hell since I have to code for a living as well.
# START COSTCO
options = Options()
options.headless = False
options.add_argument("--window-size=1920,1200")

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"

driver = webdriver.Chrome(desired_capabilities=caps, options=options, executable_path=DRIVER_PATH)
driver.get(url_costco_login)

web_username = driver.find_element_by_id("logonId")
web_password = driver.find_element_by_id("logonPassword")

web_username.send_keys(username)
web_password.send_keys(password)
driver.find_element_by_xpath("//form[@name='LogonForm']").submit()

driver.get(url_costco)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
in_stock_costco = soup.find('input', {'id': 'add-to-cart-btn'}).get('value')
in_status_costco = 'Out of Stock'
send_email(in_stock_costco, in_status_costco, url_costco, email_password, 'costco')
driver.quit()

# START BB
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

# START TARGET
options = Options()
options.headless = False
options.add_argument("--window-size=1920,1200")

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"

driver = webdriver.Chrome(desired_capabilities=caps, options=options, executable_path=DRIVER_PATH)
driver.get(url_target)
time.sleep(4)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
in_stock_target = soup.find('div', {"data-test": "storeFulfillmentAggregator"}).text.split(' in')[0]
in_status_target = 'Out of stock'
send_email(in_stock_target, in_status_target, url_target, email_password, 'target')
driver.quit()

# START SONY
options = Options()
options.headless = False
options.add_argument("--window-size=1920,1200")

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"

driver = webdriver.Chrome(desired_capabilities=caps, options=options, executable_path=DRIVER_PATH)
driver.get(url_sony)
time.sleep(3)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
in_stock_sony = soup.find('div', {"class": "button-placeholder"}).text.split('\n')[1].strip()
in_status_sony = 'Out of Stock'
send_email(in_stock_sony, in_status_sony, url_sony, email_password, 'sony direct')
driver.quit()
