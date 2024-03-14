import logging
import sys

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')

print("Printing to console: " + sys.argv[1])

logging.info("Logging an info message.")
