# Imports
import os
import logging
import sys




# Relative imports
from .. import util
from .. import submodules
from . import Article
from . import SignedArticle
from . import verify
from . import keys




# Shortcuts
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




def sign(
    article_file = None,
    public_key_dir = None,
    private_key_dir = None,
    ):
  v.validate_string(article_file)
  v.validate_string(public_key_dir)
  v.validate_string(private_key_dir)
  # Verify the article.
  article = verify.verify(
    article_file = article_file,
    article_type = 'article',
    verify_file_name = True,
    verify_signature = False,
    verify_content = True,
    verify_assets = True,
    public_key_dir = None,
  )
  # Create signature.
  author_name = article.author_name
  private_key = keys.load_private_key(private_key_dir, author_name)
  signature = gpg.make_signature(private_key, article.data)
  signature = keys.strip_gpg_signature(signature)
  data1 = '<author_signature>\n' + signature + '\n</author_signature>'
  signature = datajack.Element.from_string(data1)
  # Create signed article element.
  data2 = '<signed_article>\n</signed_article>'
  signed_article = datajack.Element.from_string(data2)
  # Insert article and signature elements into signed article.
  signed_article.insert_child(article)
  signed_article.insert_child('\n')
  signed_article.insert_child(signature)
  signed_article.insert_child('\n')
  # Create a SignedArticle from the signed article element.
  signed_article = SignedArticle.SignedArticle.from_element(signed_article)
  signed_article.set_file_path(article_file)
  # Verify signature.
  public_key = keys.load_public_key(public_key_dir, author_name)
  signed_article.verify_signature(public_key)
  return signed_article




def stop(msg=None):
  if msg is not None:
    print(msg)
  import sys
  sys.exit()
