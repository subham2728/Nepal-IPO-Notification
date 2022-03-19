import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage
import pandas as pd
import time
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

now = datetime.now()
date_time = now.strftime("%Y-%m-%d//%H:%M:%S")

load_dotenv()
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
PASSWORD = os.environ.get("PASSWORD")
PORT_NUMBER = os.environ.get("PORT_NUMBER")
URL = os.environ.get("URL")
EMAIL_SHEET_ID = os.environ.get("EMAIL_SHEET_ID")

df_sheet_email = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{EMAIL_SHEET_ID}/export?format=csv")
time.sleep(1)
print("EMAIL'S READ SUCCESSFULLY")

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
        if 'IPO' in string and 'Opening' not in string:
            string_list.append(' '.join(sub_list))

for i in range(0,len(string_list)):
  check=('\n'.join(map(str, string_list)))

print(check)

dataframe_list=pd.DataFrame({'DATE//TIME':[date_time],
                             'IPO-DATA':[string_list]
                             })

final_dataframe = pd.DataFrame([[x] + [z] for x, y in dataframe_list.values for z in y],columns=dataframe_list.columns)

# ------------------------------------------------------
#### Use this for creating new worksheet ####

# sheets.add_worksheet(title="IPO", rows=final_dataframe.shape[0], cols=final_dataframe.shape[1])

# Use this for updating values in worksheet


# ------------------------------------------------------

# ------------------------------------------------------
# Use this for appending

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/spreadsheets']

credentials = ServiceAccountCredentials.from_json_keyfile_name(r'E:\VisualStudio\Python\Nepal-IPO\service-account.json', scope)
client = gspread.authorize(credentials)

spreadsheet_id = '1g5_lAKm_S9OOnOa3IZ53O8iHA4qNREtMRfGuwiwNnuM'
sheetName = 'IPO DB'
sheets = client.open_by_key(spreadsheet_id)

values = final_dataframe.values.tolist()
sheets.values_append(sheetName, {'valueInputOption': 'USER_ENTERED'}, {'values': values})
time.sleep(1)
print("Append Successful")
# -----------------------------------------------------

# server=smtplib.SMTP('smtp.gmail.com',PORT_NUMBER)
# msg = EmailMessage()
# msg.set_content(check)
# msg['Subject'] = '[IMPORTANT] IPO OPEN!!!'
# msg['From'] = SENDER_EMAIL
# msg['To'] =df_sheet_email.loc[0,'Email']
# msg['Bcc']=df_sheet_email['Email']

# server.starttls()

# server.login(SENDER_EMAIL,PASSWORD)
# print("Login success")

# try:
#     server.send_message(msg)
#     print("Mail sent")
#     time.sleep(1)
#     print("Mail sent to : \n",df_sheet_email['Email'])
#     server.quit()
# except:
#     print("Failed to sent")

