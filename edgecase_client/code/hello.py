# Imports
import logging
import pkgutil




# Relative imports
from .. import util




# Set up logger for this module. By default, it logs at ERROR level.
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
logger.setLevel(logging.ERROR)
log = logger.info
deb = logger.debug




def setup(
    log_level = 'error',
    debug = False,
    log_timestamp = False,
    log_filepath = None,
    ):
  # Configure logger for this module.
  util.module_logger.configure_module_logger(
    logger = logger,
    logger_name = __name__,
    log_level = log_level,
    debug = debug,
    log_timestamp = log_timestamp,
    log_filepath = log_filepath,
  )
  log('Setup complete.')
  deb('Logger is logging at debug level.')




def hello():
  log('Log statement at INFO level')
  deb('Log statement at DEBUG level')
  print('hello world')




def hello_resource():
  resource_file = './resources/data1.txt'
  data1 = pkgutil.get_data(__name__, resource_file).decode('ascii')
  print(data1.strip())
