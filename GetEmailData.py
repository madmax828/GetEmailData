#------------------------------------------------------------
#   GetEmailData.py  v1.0
#   
#   This script fetches the latest 100 e‑mails from your Gmail account
#   and stores them as JSON files in a specified directory.
# 
#   Author: MaDMaX
#   Date:   2026-02-15
# 
#   Usage: 
#   python GetEmailData.py
# 
#   Optional arguments:
#   --out_dir <directory> : Directory to store JSON files (default: current folder)
# 
#   Example:
#   python GetEmailData.py --out_dir /path/to/output/directory
# 
#   Note: Make sure GMAIL_USER and GMAIL_PASS are in your .env file
# 
# ------------------------------------------------------------
# 1.  Load environment variables (credentials)
# ------------------------------------------------------------
from dotenv import load_dotenv
import os

load_dotenv()                     # reads ~/.config/.env by default
USERNAME = os.getenv('GMAIL_USER')
PASSWORD = os.getenv('GMAIL_PASS')

if not USERNAME or not PASSWORD:
    raise RuntimeError("Make sure GMAIL_USER and GMAIL_PASS are in your .env file")

# ------------------------------------------------------------
# 2.  Optional output‑directory argument (argparse)
# ------------------------------------------------------------
import argparse

parser = argparse.ArgumentParser(description="Fetch latest Gmail messages")
parser.add_argument("--out_dir", type=str, help="Directory to store JSON files (default: current folder)")
args = parser.parse_args()

output_dir = args.out_dir
if not output_dir:
    # --------------------------------------------------------
    # 3.  If no argument, pop a folder picker (tkinter)
    # --------------------------------------------------------
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()                     # hide the main window
    output_dir = filedialog.askdirectory(
        title="Select where to store fetched e‑mails"
    )
    if not output_dir:                  # user cancelled
        raise RuntimeError("No output directory selected")

# make sure the folder exists
import pathlib
output_path = pathlib.Path(output_dir)
output_path.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------
# 3.  Connect to Gmail via imapclient
# ------------------------------------------------------------
from imapclient import IMAPClient

HOST = "imap.gmail.com"
PORT = 993

client = IMAPClient(HOST, port=PORT, ssl=True)
client.login(USERNAME, PASSWORD)

# --------------------------------------------------------
# 3.  List available folders and ask user to select one
# --------------------------------------------------------
folders = client.list_folders()
folder_names = [f[2] for f in folders]

print("\nAvailable Folders:")
for idx, folder in enumerate(folder_names):
    print(f"{idx}: {folder}")

while True:
    choice = input(f"\nSelect a folder by number (0-{len(folder_names)-1}) or type the name: ").strip()
    
    if choice.isdigit():
        idx = int(choice)
        if 0 <= idx < len(folder_names):
            selected_folder = folder_names[idx]
            break
        else:
            print("Invalid number. Please try again.")
    elif choice in folder_names:
        selected_folder = choice
        break
    else:
        print("Invalid folder name. Please try again.")

print(f"\nFetching emails from: {selected_folder}")
client.select_folder(selected_folder)
uids = client.search(['ALL'])
latest_100 = uids[-100:]

import email
for uid in latest_100:
    msg_data = client.fetch([uid], ['RFC822'])
    raw_msg = msg_data[uid][b'RFC822']
    msg = email.message_from_bytes(raw_msg)

    subject = msg.get('Subject', '(no subject)')
    if isinstance(subject, bytes):
        subject = subject.decode('utf-8', errors='replace')
    
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                payload = part.get_payload(decode=True)
                if isinstance(payload, bytes):
                    body = payload.decode('utf-8', errors='replace')
                else:
                    body = payload
                break
    else:
        payload = msg.get_payload(decode=True)
        if isinstance(payload, bytes):
            body = payload.decode('utf-8', errors='replace')
        else:
            body = payload

    # --------------------------------------------------------
    # 4.  Store each message as a separate JSON file
    # --------------------------------------------------------
    data = {
        "uid": uid,
        "subject": subject,
        "body": body
    }
    json_file = output_path / f"email_{uid}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        import json
        json.dump(data, f, ensure_ascii=False)

# ------------------------------------------------------------
# 5.  Clean up
# ------------------------------------------------------------
client.logout()
print(f"Saved {len(latest_100)} emails to {output_path}")
