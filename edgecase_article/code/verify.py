# Imports
import os
import logging
import pkgutil




# Relative imports
from .. import util
from .. import submodules
from . import Article




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
    verify_file_name = None,
    verify_signature = None,
    ):
  v.validate_string(article_path)
  v.validate_string(article_type, 'article_type', 'verify.py')
  v.validate_boolean(verify_file_name)
  v.validate_boolean(verify_signature)
  if article_type != 'unspecified':
    v.validate_article_type(article_type)
  if not isfile(article_path):
    msg = "File not found at article_path {}".format(repr(article_path))
    raise ValueError(msg)
  e = datajack.Element.from_file(article_path)
  msg = "File {} contains a valid Element.".format(article_path)
  log(msg)
  v.validate_article_type(e.name, 'e.name (element name)', 'verify.py')
  if article_type == 'unspecified':
    article_type = e.name
  if e.name != article_type:
      msg = "Expected article_type {}, found element with name {}.".format(
        repr(article_type), repr(e.name),
      )
      raise ValueError(msg)
  msg = "Element name: {}.".format(e.name)
  log(msg)
  # Use the element name to select an article class.
  if article_type == 'article':
    article = Article.Article.from_element(element=e)
    article.set_file_path(article_path)
    if verify_file_name:
      article.validate_file_name()
  else:
    msg = "No class available for article_type {}".format(repr(article_type))
    raise ValueError(msg)