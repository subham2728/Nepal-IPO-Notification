import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage
import pandas as pd
import time

load_dotenv()
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
PASSWORD = os.environ.get("PASSWORD")
PORT_NUMBER = os.environ.get("PORT_NUMBER")
URL = os.environ.get("URL")
SHEET_ID = os.environ.get("SHEET_ID")

df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv")
time.sleep(1)
print("CSV READ SUCCESSFULL")
server=smtplib.SMTP('smtp.gmail.com',PORT_NUMBER)

url = URL
r = requests.get(url)
htmlContent = r.content
soup = BeautifulSoup(htmlContent, 'html.parser')
h4_tag = soup.find_all('h4')

list_ipo=[]

for tag in h4_tag:
  list_ipo.append(tag.get_text())

newList=[]

for i in list_ipo:
    newList.append(i.split())

string_list=[]

for sub_list in newList:
    for string in sub_list:
        if 'IPO' and 'Allotment' in string:
            string_list.append(' '.join(sub_list))

for i in range(0,len(string_list)):
  check=('\n'.join(map(str, string_list)))
  
print(check)

msg = EmailMessage()
msg.set_content(check)

msg['Subject'] = '[IMPORTANT] IPO OPEN!!!'
msg['From'] = SENDER_EMAIL
msg['To'] = df['Email']

server.starttls()

server.login(SENDER_EMAIL,PASSWORD)
print("Login success")

try:
    server.send_message(msg)
    print("Mail sent")
    server.quit()
except:
    print("Failed to sent")
