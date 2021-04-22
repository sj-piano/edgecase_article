# Imports
import logging




# Relative imports
from . import edgecase_client




# ### Notes
# Importing a package essentially imports the package's __init__.py file as a module.




# Collect up the things that we want in the immediate namespace of the imported datajack module.
# This file allows a script placed just above this package to run this:
# import edgecase_client
# edgecase_client.hello()
hello = edgecase_client.code.hello.hello
validate = edgecase_client.util.validate
configure_module_logger = edgecase_client.util.module_logger.configure_module_logger




# Set up logger for this module. By default, it produces no output.
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
  edgecase_client.util.module_logger.configure_module_logger(
    logger = logger,
    logger_name = __name__,
    log_level = log_level,
    debug = debug,
    log_timestamp = log_timestamp,
    log_filepath = log_filepath,
  )
  log('Setup complete.')
  deb('Logger is logging at debug level.')
  # Configure modules further down in this package.
  edgecase_client.setup(
    log_level = log_level,
    debug = debug,
    log_timestamp = log_timestamp,
    log_filepath = log_filepath,
  )
