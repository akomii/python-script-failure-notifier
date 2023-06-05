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
from pathlib import Path


def load_env_file():
    this_path = Path(os.path.realpath(__file__))
    env_file_path = os.path.join(this_path.parent, '.env')
    if os.path.isfile(env_file_path):
        with open(env_file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key] = value
    else:
        print(f"Environment file '{env_file_path}' not found.")


def send_email(subject: str, content: str):
    message = MIMEText(content)
    message['Subject'] = subject
    message['From'] = os.getenv('SENDER_EMAIL')
    message['To'] = os.getenv('RECIPIENT_EMAIL')
    with smtplib.SMTP(os.getenv('SMTP_SERVER')) as server:
        server.login(os.getenv('SMTP_USERNAME'), os.getenv('SMTP_PASSWORD'))
        server.send_message(message)


# Get the script to monitor and its input arguments from command line arguments
if len(sys.argv) < 2:
    print('Please provide the path to the script to monitor as an input argument.')
    sys.exit(1)

script_to_monitor = sys.argv[1]
script_args = sys.argv[2:]

# Load Email configuration from .env file as environment variables
load_env_file()

# Monitoring and notification
command = ['python3', script_to_monitor] + script_args
result = subprocess.run(command, capture_output=True)

if result.returncode != 0:
    error_message = f"Script '{script_to_monitor}' failed with exit code {result.returncode}.\n\n｡ﾟ･ (>﹏<) ･ﾟ｡\n\n{result.stderr.decode('utf-8')}"
    send_email('script error (╯°益°)╯彡┻━┻', error_message)
