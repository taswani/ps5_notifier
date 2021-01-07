# ps5_notifier
Python selenium script that uses automation to check the status of PS5s and get text and email notifications regarding the availability of the ps5 at Costco, Best Buy, Target, and Sony Direct. I created this in order to combat the rampant stupidity of scalpers contantly buying up all the stock of PS5s from people who just want to play video games or get their kids a PS5. I'd rather people have a notification system that gives them a leg up on where the PS5s are in stock without having the bandwidth to constantly be checking. If you aren't programmatically inclined and somehow found this, email me at tanuj.aswani@gmail.com with the numbers you want texted, and the email addresses you will like to receive the emails at, and I won't mind running it for you until you can successfully get your own PS5. 

## Requirements
Smtplib  
SSL  
Selenium  
BS4  
## Variables that need to be populated
There will be a need to have a Costco Account to access the price of the PS5 bundle. If you care not for the Costco notification, you can go ahead and delete that section of the code, as I have clearly commented the beginning of that section with START COSTCO.  
  
You will need to also enter in an email address and password for gmail, that you will use for sending out the notification. All the areas for you to input personal information has been commented clearly.  
  
Lastly, you will need to enter in the email addresses and phone numbers that you wish to send these emails and text messages out to, as well as their corresponding carrier, as I have also provided a reference guide for all the different carriers possible.  
  
You will also need to input the chromedriver path on your computer to the script before you run it. 
  

I was using windows task scheduler to have these sites checked every hour, and that's how I was able to pick up on Best Buy's restocking. If you would like help setting this up, the best thing would be to do is to start by:  
Accessing your Control Panel  
Searching for Windows Task Scheduler  
Creating a basic task within Windows task scheduler
Going through all the steps until it prompts you to choose what to do (Start a program)  
Enter ```where python``` in your command prompt and copy the path into Program/Script  
Enter the name of the script into Add Arguments (if the name of the script is the same, it would be ps5_notifier.py)
Copy the full path of the script, remove the name of the file (ps5_notifier.py) and enter it in Start in.  
Finish, and remember to run the task to get it started.  

I will update this as I remember anything else that needs to be documented. 
