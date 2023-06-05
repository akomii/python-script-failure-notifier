## python-script-failure-notifier

This project provides a script, `error_notifier.py`, that monitors the execution of another Python script and sends email notifications in case of failure. The email configuration is customizable using environment
variables. The monitoring also works with scripts that require input arguments.

### Usage:

To monitor a Python script and receive email notifications for failures, follow these steps:

Run the `error_notifier.py` script, providing the path to the script you want to monitor as an argument. You can also include any required input arguments for the script:

```
python error_notifier.py path/to/your_script.py arg1 arg2 ...
```

The `error_notifier.py` script will execute the specified script with the provided arguments. If the script fails (returns a non-zero exit code), an email notification will be sent to the configured recipient email
address.

### Configuration:

The email configuration variables can be customized by modifying the environment variables. The following variables are available:

|        Variable |          Description           |
|----------------:|:------------------------------:|
|    SENDER_EMAIL |  Email address of the sender   |
| RECIPIENT_EMAIL | Email address of the recipient |
|     SMTP_SERVER |      SMTP server address       |
|   SMTP_USERNAME |      SMTP server username      |
|   SMTP_PASSWORD |      SMTP server password      |

- The configuration variables can be passed to the script as a local file named `.env`. The file must be placed in the same directory as `error_notifier.py`:

```
SENDER_EMAIL=CHANGEME
```

- Alternatively, the environment variables can be passed to the script when it is called from the command line:

```
python error_notifier.py path/to/your_script.py arg1 --SENDER_EMAIL CHANGEME --RECIPIENT_EMAIL CHANGEME ...
```

### Testing:

To run the included test script, follow these steps:

1. Open a terminal or command prompt and navigate to the project directory.

2. Run the following command to execute the test script:

```
python -m unittest test.unit.test_error_notifier
```

The tests will run and verify the functionality of the `error_notifier.py` script by executing a script with exit code 0 and another one with exit code 1. A custom email server configuration is necessary
in the file `test/resources/.env`.

### License:

This repository is licensed under GNU Affero General Public License v3.0. See the LICENSE file for more details.
