import os
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import MySQLdb
from datetime import datetime
import google.auth.transport.requests


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
TOKEN_PICKLE = 'token.pickle'


host = 'localhost'
port = 3305
user = 'root'
password = 'sunshine123@'
database = 'email_db'



def authenticate():
    creds = None
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            flow.redirect_uri = 'http://localhost'
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PICKLE, 'wb') as token:
            pickle.dump(creds, token)
    return creds


def fetch_emails():

    conn = MySQLdb.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )

    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS emails (
        id INT AUTO_INCREMENT PRIMARY KEY,
        from_email VARCHAR(255),
        subject VARCHAR(255),
        message TEXT,
        received_date DATETIME,
        read_status BOOLEAN DEFAULT FALSE,
        folder VARCHAR(255)
    )
    """
    cursor.execute(create_table_query)

    creds = authenticate()
    service = googleapiclient.discovery.build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=50).execute()
    emails = results.get('messages', [])

    for email in emails:
        email_data = service.users().messages().get(userId='me', id=email['id']).execute()


        from_email = None
        subject = None
        message = None
        received_date = None

        headers = email_data.get('payload', {}).get('headers', [])
        for header in headers:
            name = header.get('name', '').lower()
            value = header.get('value', '')
            if name == 'from':
                from_email = value
            elif name == 'subject':
                subject = value
            elif name == 'date':

                value = value.split('(')[0].strip()
                received_date = datetime.strptime(value, '%a, %d %b %Y %H:%M:%S %z')


        insert_query = """
        INSERT INTO emails (from_email, subject, message, received_date)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (from_email, subject, message, received_date))


    conn.commit()
    conn.close()

if __name__ == '__main__':
    conn = MySQLdb.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    cursor = conn.cursor()
    fetch_emails()
    conn.close()

