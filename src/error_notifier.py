# -*- coding: utf-8 -*-
"""
Created on 02.06.23
@AUTHOR: Alexander Kombeiz (akombeiz@ukaachen.de)
@VERSION=1.03
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

import logging
import os
import smtplib
import subprocess
import sys
from email.mime.text import MIMEText
from pathlib import Path


def setup_logging(log_file_path: str):
  """Configure logging to a single file."""
  logging.basicConfig(
      filename=log_file_path,
      level=logging.INFO,
      format="%(asctime)s - %(levelname)s - %(message)s",
      datefmt="%Y-%m-%d %H:%M:%S",
  )
  console_handler = logging.StreamHandler(sys.stdout)
  console_handler.setLevel(logging.INFO)
  formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
  console_handler.setFormatter(formatter)
  logging.getLogger().addHandler(console_handler)


def check_env_variables() -> list[str]:
  keys = ["SENDER_EMAIL", "RECIPIENT_EMAIL", "SMTP_SERVER", "SMTP_USERNAME", "SMTP_PASSWORD"]
  missing_keys = [key for key in keys if key not in os.environ]
  return missing_keys


def load_env_file():
  """Load environment variables from a .env file if missing."""
  env_path = Path(__file__).parent / ".env"
  if not env_path.exists():
    raise FileNotFoundError(f"Environment file '{env_path}' not found.")
  with open(env_path, "r") as file:
    for line in file:
      line = line.strip()
      if line and not line.startswith("#"):
        key, value = line.split("=", 1)
        os.environ[key] = value


def send_email(subject: str, content: str):
  try:
    message = MIMEText(content)
    message["Subject"] = subject
    message["From"] = os.getenv("SENDER_EMAIL")
    message["To"] = os.getenv("RECIPIENT_EMAIL")
    with smtplib.SMTP_SSL(os.getenv("SMTP_SERVER")) as server:
      server.login(os.getenv("SMTP_USERNAME"), os.getenv("SMTP_PASSWORD"))
      server.send_message(message)
    logging.info("Error notification email sent successfully.")
  except Exception as e:
    logging.error(f"Failed to send email: {e}")


def read_log_file(log_file_path: str) -> str:
  try:
    with open(log_file_path, "r") as file:
      return file.read()
  except Exception as e:
    logging.error(f"Failed to read log file: {e}")
    return f"Could not read log file: {e}"

def main():
  if len(sys.argv) < 3:
    print("Usage: error_notifier.py <log_file_path> <script_to_monitor> [script_args...]")
    sys.exit(1)
  log_file_path = sys.argv[1]
  script_to_monitor = sys.argv[2]
  script_args = sys.argv[3:]

  # Setup logging
  setup_logging(log_file_path)

  # Check for environment variables and load from file if missing
  missing_keys = check_env_variables()
  if missing_keys:
    logging.warning(f"Missing environment variables: {missing_keys}. Attempting to load from .env")
    load_env_file()
    missing_keys = check_env_variables()
    if missing_keys:
      logging.error(f"Missing required environment variables after loading: {missing_keys}")
      sys.exit(1)

  # Run the monitored script
  command = ["python3", script_to_monitor] + script_args
  logging.info(f"Executing command: {' '.join(command)}")
  with open(log_file_path, "w+") as log_file:
    result = subprocess.run(command, stdout=log_file, stderr=log_file, text=True)
  if result.returncode != 0:
    log_content = read_log_file(log_file_path)
    email_body = (
      f"Script '{script_to_monitor}' failed with exit code {result.returncode}.\n\n"
      f"----- LOG OUTPUT -----\n{log_content}\n"
      f"----------------------"
    )
    logging.error(f"Script failed. Sending email notification.")
    send_email("Script error (╯°益°)╯彡┻━┻", email_body)


if __name__ == '__main__':
  main()
