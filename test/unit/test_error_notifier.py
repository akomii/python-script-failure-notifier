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
        cls.__PATH_TEST_RESOURCES = os.path.join(this_path.parents[1], 'resources')
        cls.load_test_env_file()

    @classmethod
    def tearDownClass(cls):
        for file in os.listdir(cls.__PATH_TEST_RESOURCES):
            if file.endswith('.log') or file.endswith('.log.err'):
                os.remove(os.path.join(cls.__PATH_TEST_RESOURCES, file))

    def run_script_with_logging(self, script_name, *args):
        path_script = os.path.join(self.__PATH_TEST_RESOURCES, script_name)
        script_base_name = os.path.splitext(script_name)[0]
        path_log = os.path.join(self.__PATH_TEST_RESOURCES, f"{script_base_name}.log")
        command = ['python3', self.__PATH_ERROR_NOTIFIER, path_log, path_script] + list(args)
        subprocess.run(command, env=os.environ)

    def test_script(self):
        self.run_script_with_logging('info_logging.py', 'Hello World')
        self.run_script_with_logging('error_logging.py', 'Hello World')
        self.run_script_with_logging('exception.py')
        self.run_script_with_logging('systemexit.py')


if __name__ == '__main__':
    unittest.main()
