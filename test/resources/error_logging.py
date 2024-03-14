import logging
import sys

logging.basicConfig(level=logging.ERROR, format='%(levelname)s:%(message)s')

print("Printing to console: " + sys.argv[1])

logging.error("Logging an error message.")
