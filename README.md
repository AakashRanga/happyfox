# happyfox

Starting with installing required libraries
=> pip install requirements.txt

Authenticate to Google’s GMail API and save to local Database,

<img width="960" alt="capture2" src="https://github.com/AakashRanga/happyfox/assets/105368559/c6ab78ee-efcd-4927-b860-e5f3dbaea67f">


For the first three process I have used fetch_email.py file
The File contains authenticate() for Gmail API to check user and Authentication 
Since this is standalone Python script, not a web server project, Somehow I tried to manage to run with this 'http://localhost' to redirect.
Later on After completing the authentication the Fetch email creates a Table based on given server conn details
Then I have set maxResults to 50 to collect the mail from my Inbox.
And finally Inserting into my Table.



<img width="960" alt="capture3" src="https://github.com/Aakash287/learning_material/assets/119830681/03203ca7-e909-419d-afa0-ddbbf6b970db">




Next Process,

Process Emails based on requirement rules,

Based on the given condition I have made seperate file for processing the emails in process_email.py
There first I am running the JSON file which has all set of rules inside it in JSON format.
After opening the file I am Iterating the data from it and keep in separate variables 
Based on Any/All the task is set to find different conditions 
If it is All it will check if both email and subject matches the same and gets the actions based on rule (AND).
If it is Any it will check any of the condition satisfies and gets the action based on rule (OR).
I have all the conditions rules in JSON file itself to execute the code.




<img width="960" alt="capture4" src="https://github.com/Aakash287/learning_material/assets/119830681/1e83e1a6-b72e-4b81-b208-dacdd3f95839">

