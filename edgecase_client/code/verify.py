# Imports
import os
import logging
import pkgutil




# Relative imports
from .. import util
from .. import submodules




# Shortcuts
isfile = os.path.isfile
v = util.validate
datajack = submodules.datajack
stateless_gpg = submodules.stateless_gpg
gpg = stateless_gpg.gpg




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




def verify(
    article_path = None,
    article_type = None,
  ):
  v.string(article_path)
  v.string(article_type)
  article_types = ("article signed_article checkpoint_article" + \
    " datafeed_article signed_datafeed_article"
  ).split()
  if article_type != 'unspecified' and article_type not in article_types:
    msg = "Unrecognised article_type: {}".format(article_type)
    raise ValueError(msg)
  if not isfile(article_path):
    msg = "File not found at article_path {}".format(repr(article_path))
    raise ValueError(msg)
  e = datajack.Element.from_file(article_path)
  msg = "File {} contains a valid Element.".format(article_path)
  log(msg)
  if article_type == 'unspecified':
    if e.name not in article_types:
      msg = "Element name {} not in list of recognised article_types".format(repr(e.name))
      msg += "\n{}".format(article_types)
      raise ValueError(msg)
  elif e.name != article_type:
      msg = "Expected article_type {}, found element with name {}.".format(
        repr(article_type), repr(e.name),
      )
      raise ValueError(msg)
  msg = "Element name: {}.".format(e.name)
  log(msg)
  # Use the element name to select an article class.











