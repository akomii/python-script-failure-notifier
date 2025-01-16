# -*- coding: utf-8 -*-
"""
Created on 02.06.23
@AUTHOR: Alexander Kombeiz (akombeiz@ukaachen.de)
@VERSION=1.02
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


def check_env_variables_for_required_keys() -> list[str]:
    keys = ["SENDER_EMAIL", "RECIPIENT_EMAIL", "SMTP_SERVER", "SMTP_USERNAME", "SMTP_PASSWORD"]
    missing_keys = [key for key in keys if key not in os.environ]
    return missing_keys


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
        raise FileNotFoundError(
            f"Environment file  '{env_file_path}' not found.")


def ensure_log_file_exists(log_file_path):
    if not os.path.exists(log_file_path):
        with open(log_file_path, 'a') as f:
            f.write('')


def send_email(subject: str, content: str):
    message = MIMEText(content)
    message['Subject'] = subject
    message['From'] = os.getenv('SENDER_EMAIL')
    message['To'] = os.getenv('RECIPIENT_EMAIL')
    with smtplib.SMTP_SSL(os.getenv('SMTP_SERVER')) as server:
        server.login(os.getenv('SMTP_USERNAME'), os.getenv('SMTP_PASSWORD'))
        server.send_message(message)


def main():
    if len(sys.argv) < 3:
        print('Usage: error_notifier.py <log_file_path> <script_to_monitor> [script_args...]')
        sys.exit(1)

    log_file_path = sys.argv[1]
    script_to_monitor = sys.argv[2]
    script_args = sys.argv[3:]

    # Check for environment variables and load from file if necessary
    are_keys_missing = check_env_variables_for_required_keys()
    if are_keys_missing:
        load_env_file()

    # Monitoring and notification
    ensure_log_file_exists(log_file_path)
    command = ['python3', script_to_monitor] + script_args
    with open(log_file_path, "w") as log_file, open(log_file_path + ".err", "w+") as err_file:
        result = subprocess.run(command, stdout=log_file, stderr=err_file, text=True)
        err_file.seek(0)
        errors = err_file.read()
        if result.returncode != 0 and errors:
            error_message = f"Script '{script_to_monitor}' failed with exit code {result.returncode}.\n\n｡ﾟ･ (>﹏<) ･ﾟ｡\n\n{errors}"
            send_email('Script error (╯°益°)╯彡┻━┻', error_message)


if __name__ == '__main__':
    main()
