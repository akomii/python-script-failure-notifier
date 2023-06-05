import os
import subprocess
import unittest
from pathlib import Path


class TestErrorNotifier(unittest.TestCase):

    @classmethod
    def load_test_env_file(cls):
        this_path = Path(os.path.realpath(__file__))
        path_test_env = os.path.join(this_path.parents[1], 'resources', '.env')
        with open(path_test_env) as env:
            for line in env:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key] = value

    @classmethod
    def setUpClass(cls):
        this_path = Path(os.path.realpath(__file__))
        path_src = os.path.join(this_path.parents[2], 'src')
        cls.__PATH_ERROR_NOTIFIER = os.path.join(path_src, 'error_notifier.py')
        path_test_resources = os.path.join(this_path.parents[1], 'resources')
        cls.__PATH_SUCCESS_SCRIPT = os.path.join(path_test_resources, 'script_that_succeds.py')
        cls.__PATH_FAILURE_SCRIPT = os.path.join(path_test_resources, 'script_that_fails.py')
        cls.load_test_env_file()

    def test_success_script(self):
        command = ['python3', self.__PATH_ERROR_NOTIFIER, self.__PATH_SUCCESS_SCRIPT, 'Hello World']
        subprocess.run(command, env=os.environ)

    def test_failure_script(self):
        command = ['python3', self.__PATH_ERROR_NOTIFIER, self.__PATH_FAILURE_SCRIPT]
        subprocess.run(command, env=os.environ)


if __name__ == '__main__':
    unittest.main()
