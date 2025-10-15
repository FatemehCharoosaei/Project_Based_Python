import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import csv
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
# Your email credentials - with proper error handling
sender_email = os.getenv("Email_Username")
sender_password = os.getenv("Email_App_Password")
# Check if environment variables are loaded properly
if not sender_email or not sender_password:
   print("ERROR: Email credentials not found!")
   print("Please make sure Email_Username and Email_App_Password are set in your environment variables or .env file")
   exit(1)
# Path to your CSV file
csv_file_path = "recipients2_2.csv"
# Verify CSV file exists
if not os.path.exists(csv_file_path):
   print(f"ERROR: CSV file '{csv_file_path}' not found!")
   exit(1)
# List of inspirational quotes
quotes = [
   "The best way to predict the future is to invent it. – Alan Kay",
   "A dream doesn't become reality through magic; it takes sweat, determination, and hard work. – Colin Powell",
   "Success is not the key to happiness. Happiness is the key to success. If you love what you are doing, you will be successful. – Albert Schweitzer",
   # Add more quotes as needed
]
# Function to send emails
def send_email(recipient_name, recipient_email, quote):
   subject = "Your Daily Inspirational Quote"
   body = f"Hello {recipient_name}, here is your daily inspirational quote:\n\n{quote}"
   # Setting up the MIME
   message = MIMEMultipart()
   message['From'] = sender_email
   message['To'] = recipient_email
   message['Subject'] = subject
   message.attach(MIMEText(body, 'plain'))
   # Sending the email
   try:
       session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
       session.starttls()  # enable security
       session.login(sender_email, sender_password)  # login with mail_id and password
       text = message.as_string()
       session.sendmail(sender_email, recipient_email, text)
       session.quit()
       print(f"✓ Mail Sent Successfully to {recipient_name} ({recipient_email})")
       return True
   except Exception as e:
       print(f"✗ Failed to send email to {recipient_name} ({recipient_email}). Error: {e}")
       return False
# Read CSV and send emails
try:
   with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
       reader = csv.DictReader(csvfile)
       
       # Check if CSV has required columns
       if 'name' not in reader.fieldnames or 'email' not in reader.fieldnames:
           print("ERROR: CSV file must contain 'name' and 'email' columns!")
           exit(1)
       
       success_count = 0
       fail_count = 0
       
       for row in reader:
           recipient_name = row['name'].strip()
           recipient_email = row['email'].strip()
           
           # Validate email format
           if not recipient_email or '@' not in recipient_email:
               print(f"✗ Invalid email format for {recipient_name}: {recipient_email}")
               fail_count += 1
               continue
           
           # Select a random quote
           quote_of_the_day = random.choice(quotes)
           
           if send_email(recipient_name, recipient_email, quote_of_the_day):
               success_count += 1
           else:
               fail_count += 1
   print(f"\n📊 Summary: {success_count} emails sent successfully, {fail_count} failed")
except FileNotFoundError:
   print(f"ERROR: CSV file '{csv_file_path}' not found!")
except Exception as e:
   print(f"ERROR reading CSV file: {e}")