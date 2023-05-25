import json
import MySQLdb
from datetime import datetime

host = 'localhost'
port = 3305
user = 'root'
password = 'sunshine123@'
database = 'email_db'

def process_emails(rules_file):

    with open(rules_file) as file:
        data = json.load(file)
        rules = data['rules']


    conn = MySQLdb.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    cursor = conn.cursor()


    select_query = """
    SELECT id, from_email, subject, message, received_date, read_status, folder
    FROM emails
    """
    cursor.execute(select_query)
    emails = cursor.fetchall()

    for email in emails:
        email_id, from_email, subject, message, received_date, read_status, folder = email

        for rule in rules:
            predicate = rule['predicate']
            conditions = rule['conditions']
            actions = rule['actions']

            if (predicate == 'All' and all(check_condition(condition, email) for condition in conditions)) or \
                    (predicate == 'Any' and any(check_condition(condition, email) for condition in conditions)):
                perform_actions(actions, email_id, cursor)

    conn.commit()
    conn.close()

def check_condition(condition, email):
    field_name = condition['field']
    predicate = condition['predicate']
    value = condition['value']


    if field_name == 'From':
        field_value = email[1]
    elif field_name == 'Subject':
        field_value = email[2]
    elif field_name == 'Message':
        field_value = email[3]
    elif field_name == 'Received Date/Time':
        field_value = email[4]
        value = datetime.strptime(value, '%Y-%m-%d')

    if predicate == 'Contains':
        return value in field_value
    elif predicate == 'Does not Contain':
        return value not in field_value
    elif predicate == 'Equals':
        return value == field_value
    elif predicate == 'Does not equal':
        return value != field_value
    elif predicate == 'Less than':
        return field_value < value
    elif predicate == 'Greater than':
        return field_value > value

def perform_actions(actions, email_id, cursor):
    for action in actions:
        if action == 'Mark as read':
            update_query = """
            UPDATE emails
            SET read_status = TRUE
            WHERE id = %s
            """
            cursor.execute(update_query, (email_id,))
        elif action == 'Mark as unread':
            update_query = """
            UPDATE emails
            SET read_status = FALSE
            WHERE id = %s
            """
            cursor.execute(update_query, (email_id,))
        elif action == 'Move Message':
            update_query = """
            UPDATE emails
            SET folder = 'Archive'
            WHERE id = %s
            """
            cursor.execute(update_query, (email_id,))
        elif action == 'print_details':
            select_query = """
            SELECT id, from_email, subject, message, received_date, read_status, folder
            FROM emails
            WHERE id = %s
            """
            cursor.execute(select_query, (email_id,))
            email = cursor.fetchone()
            email_id, from_email, subject, message, received_date, read_status, folder = email
            print("Email Details:")
            print("ID:", email_id)
            print("From:", from_email)
            print("Subject:", subject)
            print("Message:", message)
            print("Received Date:", received_date)
            print("Read Status:", read_status)
            print("Folder:", folder)


if __name__ == '__main__':
    process_emails('rules.json')
