from __future__ import print_function

import os.path
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'


def grab():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    timestamp = timestamp - 86400
    #dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
    #print(dt_string)
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    try:
        service = build('sheets', 'v4', credentials=creds)
        # SAMPLE_SPREADSHEET_ID , ,range="A1:C3"
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId="1sCKHKtqBrtKVGD909wi7BiynqXccow1GfqB0ASnFQGA",
                                    range="Form Responses 1").execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return
        
        #STRIP THE FIRST ROW
        values = values[1:]
        
        retvaluesP = []
        retvaluesN = []
        
        #print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            pstr = ""
            #datetime.timestamp(row[0])
            date_obj = datetime.strptime(row[0], "%m/%d/%Y %H:%M:%S")
            subtime = datetime.timestamp(date_obj)
            #pstr+= str(subtime) + " "
            #Strip date
            row = row[1:]
            if(timestamp<= subtime):
                i=0
                for col in row:
                    if(i%2==0):
                        retvaluesP.append(col)
                    else:
                        retvaluesN.append(col)
                    pstr+=col + " "
                    i+=1
            #print('%s, %s, %s' % (row[0],row[1], row[2]))
            print(pstr)
    except HttpError as err:
        print(err)
    return retvaluesP , retvaluesN