# -*- coding: utf-8 -*-
"""
Created on 02.06.23
@AUTHOR: Alexander Kombeiz (akombeiz@ukaachen.de)
@VERSION=1.0
"""

#
#      Copyright (c) 2023 Alexander Kombeiz
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU Affero General Public License as
#      published by the Free Software Foundation, either version 3 of the
#      License, or (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU Affero General Public License for more details.
#
#      You should have received a copy of the GNU Affero General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#

import os
import smtplib
import subprocess
import sys
from email.mime.text import MIMEText

# Email Configuration, environment variables are used to allow easier testing
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL')

SMTP_SERVER = os.environ.get('SMTP_SERVER')
SMTP_USERNAME = os.environ.get('SMTP_USERNAME')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')


# Function to send email notifications
def send_email(subject: str, content: str):
    message = MIMEText(content)
    message['Subject'] = subject
    message['From'] = SENDER_EMAIL
    message['To'] = RECIPIENT_EMAIL

    with smtplib.SMTP(SMTP_SERVER) as server:
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(message)


# Get the script to monitor and its input arguments from command line arguments
if len(sys.argv) < 2:
    print('Please provide the path to the script to monitor as an input argument.')
    sys.exit(1)

script_to_monitor = sys.argv[1]
script_args = sys.argv[2:]

# Monitoring and notification
command = ['python3', script_to_monitor] + script_args
result = subprocess.run(command, capture_output=True)

if result.returncode != 0:
    error_message = f"Script '{script_to_monitor}' failed with exit code {result.returncode}.\n\n｡ﾟ･ (>﹏<) ･ﾟ｡\n\n{result.stderr.decode('utf-8')}"
    send_email('script error (╯°益°)╯彡┻━┻', error_message)
