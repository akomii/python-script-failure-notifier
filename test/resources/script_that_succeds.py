import logging
import sys

try:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', handlers=[logging.StreamHandler()])
    print(sys.argv[1])
    logging.info(sys.argv[1])
finally:
    [logging.root.removeHandler(handler) for handler in logging.root.handlers[:]]
    logging.shutdown()
