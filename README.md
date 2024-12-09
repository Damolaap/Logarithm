# Educational Scripts for Networking and Monitoring
  Disclaimer: These scripts are intended for educational purposes only. Unauthorized use for malicious purposes is illegal and unethical. Use responsibly and with explicit consent.

# Scripts Included
Educational Keylogger Script
HTTP File Server Script

# 1. Educational Keylogger Script
This script demonstrates keylogging and clipboard monitoring techniques. It logs keystrokes, monitors clipboard data, and sends periodic updates via email. Additionally, it can register itself for automatic startup.

# Features
Logs keystrokes with timestamps and active window titles.
Monitors clipboard changes.
Periodically emails logs to a recipient.
Registers itself in the Windows startup registry.

# Requirements
Python 3.8+
Required modules:
pynput
pyperclip
python-dotenv
pywin32
smtplib
Install dependencies:

pip install pynput pyperclip python-dotenv pywin32

# 2. HTTP File Server Script
This script serves as a basic HTTP server for sharing files over the network. It allows users to download a specified file from the host machine using a browser.

# Features
Hosts a file for download via an HTTP server.
Automatically determines the local IP address for sharing on the network.
Supports file download with Content-Disposition headers for proper handling by the browser.

# Requirements
Python 3.6+
No additional modules required (uses Python's built-in libraries).

# Compiling to an Executable
To make the scripts more portable, you can compile them into executables using PyInstaller.

Steps:
Install PyInstaller:

pip install pyinstaller
Navigate to the script's directory and run the following command:

pyinstaller --onefile --add-data ".env;." script_name.py

Replace script_name.py with the actual script name (e.g., svchost.py).
The --add-data flag ensures the .env file is included in the executable.
The compiled executable will be located in the dist folder.

# Tips:
Ensure the .env file is in the same directory as the script during compilation.
For the keylogger, test the executable in a controlled environment to verify startup behavior and email functionality.
Future Enhancements
New features will be added to both scripts, such as:
Enhanced logging options.
Encrypted communication for secure email transmission.
A user-friendly web interface for the file server.
Stay tuned for updates and improvements!
