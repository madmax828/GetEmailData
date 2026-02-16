Created this to download your emails to use for AI training or whatever else you may need it for.

---------Follow This First to setup your Gmail to accept IMAP requests --------------

For creditials in the .env you have to set up an App Password on your gmail account. 
You must first ensure that 2-Step Verification is enabled on the Google account. 

Step 1: Enable 2-Step Verification 
If you already have 2-Step Verification active, skip to Step 2. 

- Go to your Google Account settings.
  Select Security on the left-hand menu.
  Under "How you sign in to Google," click on 2-Step Verification.
  Follow the prompts to turn it on. 

Step 2: Generate the App Password
- Google recently updated their interface; if you cannot find "App Passwords" by clicking through menus, the 
  search bar method is the fastest. 
  In your Google Account, click the Search bar at the top.
  Type "App passwords" and select the result that appears.
  Enter a custom name for the app (e.g., "Outlook Desktop" or "My IMAP App").
  Click Create.
  A window will pop up with a 16-character code (the App Password).

Note: Copy this immediately; you will not be able to see it again.
Click Done. 

Step 3: Use the Password in Your App 
- When configuring your IMAP application, use the following credentials:

        Username: (YourFullGmail@gmail.com)
        Password: The 16-character code you just generated (Do NOT use your regular Gmail password).
        IMAP Server: imap.gmail.com
        Port: 993 (SSL/TLS) 

Important: Make sure IMAP Access is enabled in your Gmail settings. Go to Gmail > Settings > Forwarding and POP/IMAP > Enable IMAP.

# GetEmailData
Fetches the latest 100 e‑mails from your Gmail account and stores them as JSON files in a specified directory of your choosing.

    ------------Requirements.txt-----------------
      Windows: python.exe -m pip install -r requirements.txt
      Mac/Linux: python3 -m pip install -r requirements.txt

      Usage: 
         Windows: python.exe GetEmailData.py
         Mac/Linux: python3 GetEmailData.py
         
      Optional arguments:
         --out_dir <directory> : Directory to store JSON files (default: current folder)
 
     Example:
         Windows: python.exe GetEmailData.py --out_dir /path/to/output/directory
         Mac/Linux: python3 GetEmailData.py --out_dir /path/to/output/directory

 Note: Make sure GMAIL_USER and GMAIL_PASS are in your .env file



