# Imports
import logging




# Relative imports
from .. import util
from . import datajack
from . import stateless_gpg




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
    log_file = None,
    ):
  # Configure logger for this module.
  util.module_logger.configure_module_logger(
    logger = logger,
    logger_name = __name__,
    log_level = log_level,
    debug = debug,
    log_timestamp = log_timestamp,
    log_file = log_file,
  )
  deb('Setup complete.')
  # Configure modules further down in this package.
  datajack.setup(
    log_level = log_level,
    debug = debug,
    log_timestamp = log_timestamp,
    log_file = log_file,
  )
  stateless_gpg.setup(
    log_level = log_level,
    debug = debug,
    log_timestamp = log_timestamp,
    log_file = log_file,
  )
