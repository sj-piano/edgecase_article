# Imports
import os
import logging




# Relative imports
from .. import util
from .. import submodules
from . import DatafeedArticle




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




class SignedDatafeedArticle(datajack.Element):


  @classmethod
  def from_element(cls, element):
    e = element.create_copy()
    e.__class__ = SignedDatafeedArticle
    e.datafeed_article = DatafeedArticle.DatafeedArticle.from_element(e.get_one('datafeed_article'))
    e.datafeed_signature = e.get_one('datafeed_signature')
    e.article = e.datafeed_article.article
    e.article_type = 'signed_datafeed_article'
    e.file_path = None
    e.file_name = None
    e.validate_format()
    return e


  def __str__(self):
    return 'SignedDatafeedArticle: [{t}]'.format(t=self.title)


  @property
  def datafeed_name(self):
    return self.datafeed_article.datafeed_name


  @property
  def datafeed_article_id(self):
    return self.datafeed_article.datafeed_article_id


  @property
  def daid(self):
    return self.datafeed_article.daid


  @property
  def title(self):
    return self.article.title


  @property
  def uri_title(self):
    return self.article.uri_title


  @property
  def author_name(self):
    return self.article.author_name


  @property
  def date(self):
    return self.datafeed_article.date


  @property
  def gpg_signature(self):
    data = self.datafeed_signature.text
    data = data.strip()
    s = '-----BEGIN PGP SIGNATURE-----\n\n'
    s += data
    s += '\n-----END PGP SIGNATURE-----\n'
    return s


  @property
  def previous_checkpoint(self):
    return self.datafeed_article.previous_checkpoint


  @property
  def content_element(self):
    return self.article.content_element


  def validate_format(self):
    names = sorted(self.element_children_names)
    expected = 'datafeed_article datafeed_signature'
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
    self.datafeed_article.file_path = file_path
    self.datafeed_article.file_name = file_name


  def validate_file_name(self):
    self.datafeed_article.validate_file_name()


  def verify_signature(self, public_key):
    # The public key must be that of the datafeed.
    data = self.datafeed_article.escaped_data
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
