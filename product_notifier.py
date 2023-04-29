import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import time


class ProductNotifier:
    def __init__(self, phone_number, email_address, email_password, recipients, seller, url, product):
        self.phone_number = phone_number
        self.email_address = email_address
        self.email_password = email_password
        self.recipients = recipients # Has to be in the shape of an array
        self.in_stock_text = ""
        self.current_status_text = ['Sold Out', 'Coming Soon']
        self.seller = seller
        self.url = url
        self.product = product

        self.email_config = {}
        self.DRIVER = None
        self.DRIVER_PATH = './chromedriver.exe' #Put the path to your chromedriver here, for example: C:/Users/*YourUsernameHere*/Desktop/chromedriver.exe

    def _setup_email(self):
        self.email_config["port"] = 465  # For SSL
        self.email_config["smtp_server"] = "smtp.gmail.com"
        self.email_config["sender_email"] = self.email_address  # Enter your gmail address
        self.email_config["receiver_email"] = self.recipients  # Enter receivers email addresses
        self.email_config["password"] = self.email_password
        self.email_config["message"] = """Subject: {} {} at {}!\n\n
            {} {} at {}.""".format(self.product, self.in_stock_text, self.seller, self.product, self.in_stock_text, self.url)
            
    def _setup_att_text_message(self):
        # TODO: Add feature to send texts to multiple recipients based off of carrier
        msg = MIMEMultipart()
        sms_gateway = '{}@txt.att.net'.format(self.phone_number) #put your att phone number before the @ symbol
        msg['From'] = self.email_config["sender_email"]
        msg['To'] = sms_gateway
        # Make sure you add a new line in the subject
        msg['Subject'] = "Subject: {} {} {}!\n".format(self.product, self.in_stock_text, self.seller)
        # Make sure you also add new lines to your body
        body = "{} {} at {}.".format(self.product, self.in_stock_text, self.url)
        # and then attach that body furthermore you can also send html content.
        msg.attach(MIMEText(body, 'plain'))
        sms = msg.as_string()

        return [sms_gateway, sms]

    def send_messages(self):
        '''
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
        
        self._setup_email()

        if self.in_stock_text not in self.current_status_text:
            # Create a secure SSL context
            context = ssl.create_default_context()

            with smtplib.SMTP_SSL(self.email_config["smtp_server"], self.email_config["port"], context=context) as server:
                server.login(self.email_config["sender_email"], self.email_config["password"])
                # Email
                server.sendmail(self.email_config["sender_email"], self.email_config["receiver_email"], self.email_config["message"])

                # Text Messaging
                sms_gateway, sms = self._setup_att_text_message()

                server.sendmail(self.email_config["sender_email"], sms_gateway, sms)
            
            print("Email has been sent!")
        
        print("Email was not sent.")

    def _setup_selenium(self):
        options = Options()
        options.headless = False
        options.add_argument("--window-size=1920,1200")

        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"

        self.DRIVER = webdriver.Chrome(desired_capabilities=caps, options=options, executable_path=self.DRIVER_PATH)

    def _set_in_stock_text(self):
        self.DRIVER.get(self.url)
        time.sleep(2)
        html = self.DRIVER.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # This will only work given that there is a add-to-cart-button class in the right spot (AKA only works for Best Buy)
        # TODO: Extend this logic to match references to add-to-cart text/classes/ids
        self.in_stock_text = soup.find('button', {"class": "add-to-cart-button"}).text

    def run_product_notifier(self):
        self._setup_selenium()
        self._set_in_stock_text()
        self.send_messages()
        self.DRIVER.quit()


if __name__ == "__main__":
    # setup config
    notifier_params = {
        "phone_number": "",
        "email_address": "",
        "email_password": "", # Generated app password
        "recipients": [],
        "seller": "",
        "url": "",
        "product": ""
    }

    # instantiate
    best_buy_product_notifier = ProductNotifier(
        notifier_params["phone_number"],
        notifier_params["email_address"],
        notifier_params["email_password"],
        notifier_params["recipients"],
        notifier_params["seller"],
        notifier_params["url"],
        notifier_params["product"],
    )
    best_buy_product_notifier.run_product_notifier()