# Imports
import os
import logging
import pkgutil




# Relative imports
from .. import util
from .. import submodules
from . import Article
from . import SignedArticle
from . import CheckpointArticle
from . import DatafeedArticle
from . import SignedDatafeedArticle




# Shortcuts
v = util.validate
datajack = submodules.datajack




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
    public_key_dir = None,
    ):
  v.validate_string(article_path)
  v.validate_string(article_type, 'article_type', 'verify.py')
  v.validate_boolean(verify_file_name)
  v.validate_boolean(verify_signature)
  if article_type != 'unspecified':
    v.validate_article_type(article_type)
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
  msg = "Element name: {}".format(e.name)
  log(msg)
  # Use the element name to select an article class.
  a = None
  if article_type == 'article':
    a = Article.Article.from_element(element=e)
  elif article_type == 'signed_article':
    a = SignedArticle.SignedArticle.from_element(element=e)
  elif article_type == 'checkpoint_article':
    a = CheckpointArticle.CheckpointArticle.from_element(element=e)
  elif article_type == 'datafeed_article':
    a = DatafeedArticle.DatafeedArticle.from_element(element=e)
  elif article_type == 'signed_datafeed_article':
    a = SignedDatafeedArticle.SignedDatafeedArticle.from_element(element=e)
  else:
    msg = "No class available for article_type {}".format(repr(article_type))
    raise ValueError(msg)
  a.set_file_path(article_path)
  if verify_file_name:
    a.validate_file_name()
  if verify_signature:
    if a.article_type == 'signed_article':
      author_name = a.author_name
      public_key = load_public_key(public_key_dir, author_name)
      a.verify_signature(public_key)
    elif a.article_type == 'signed_datafeed_article':
      datafeed_name = 'edgecase_datafeed'  # hardcoded.
      public_key = load_public_key(public_key_dir, datafeed_name)
      a.verify_signature(public_key)
    else:
      msg = "verifySignature not possible for article_type {}".format(repr(a.article_type))
      raise ValueError(msg)
    msg = "Signature verified for {}".format(a.__class__.__name__)
    log(msg)




def load_public_key(public_key_dir, author_name):
  # Example public key file name:
  # stjohn_piano_public_key.txt
  pk_ext = '_public_key.txt'
  items = os.listdir(public_key_dir)
  key_file_names = [x for x in items if os.path.splitext(x)[1] == '.txt']
  author_names = [x.replace(pk_ext, '') for x in key_file_names]
  if author_name not in author_names:
    msg = "Did not find any public key with author name {} in public key directory {}.".format(repr(author_name), repr(public_key_dir))
    raise FileNotFoundError(msg)
  key_file_name = author_name + pk_ext
  key_file = os.path.join(public_key_dir, key_file_name)
  public_key = open(key_file).read().strip()
  return public_key
