# Imports
import os
import logging




# Relative imports
from .. import util
from .. import submodules
from . import Article




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




class SignedArticle(datajack.Element):


  @classmethod
  def from_element(cls, element):
    e = element
    e.__class__ = SignedArticle
    e.validate_format()
    e.article_type = 'signed_article'
    e.file_path = None
    e.file_name = None
    e.article = Article.Article.from_element(e.get_one('article'))
    e.author_signature = e.get_one('author_signature')
    return e


  def __str__(self):
    return 'SignedArticle: [{t}]'.format(t=self.title)


  def validate_format(self):
    names = sorted(self.element_children_names)
    expected = 'article author_signature'
    expected = sorted(expected.split())
    if names != expected:
      msg = "Found these child elements: "
      msg += ''.join(['\n- ' + x for x in names])
      msg += '\nBut expected these child elements:'
      msg += ''.join(['\n- ' + x for x in expected])
      raise ValueError(msg)


  def set_file_path(self, file_path):
    v.validate_string(file_path)
    self.file_path = file_path
    file_name = os.path.basename(file_path)
    self.file_name = file_name
    # Also set these values for child elements.
    self.article.file_path = file_path
    self.article.file_name = file_name


  def validate_file_name(self):
    self.article.validate_file_name()


  @property
  def title(self):
    return self.article.title


  @property
  def uri_title(self):
    return util.misc.uri_title(self.title)


  @property
  def author_name(self):
    return self.article.author_name


  @property
  def date(self):
    return self.article.date


  @property
  def signed_by_author(self):
    return self.article.signed_by_author


  @property
  def gpg_signature(self):
    data = self.author_signature.text
    data = data.strip()
    s = '-----BEGIN PGP SIGNATURE-----\n\n'
    s += data
    s += '\n-----END PGP SIGNATURE-----\n'
    return s


  def verify_signature(self, public_key):
    # The public key must be that of the author.
    data = self.article.escaped_data
    signature = self.gpg_signature
    result = gpg.verify_signature(
      public_key,
      data,
      signature,
    )
    if result is not True:
      msg = "Invalid signature"
      raise ValueError(msg)
    return result
