# Imports
import os
import logging




# Relative imports
from .. import util
from .. import submodules




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
  deb('Setup complete.')




class Article(datajack.Element):


  def __init__(self):
    pass


  @classmethod
  def from_element(cls, element):
    e = element
    e.__class__ = Article
    e.validate_format()
    e.article_type = 'article'
    e.file_path = None
    e.file_name = None
    return e


  def __str__(self):
    return 'Article: [{t}]'.format(t=self.title)


  @property
  def title(self):
    return self.get_value('title')


  @property
  def uri_title(self):
    return util.misc.uri_title(self.title)


  @property
  def author_name(self):
    return self.get_value('author_name')


  @property
  def date(self):
    return self.get_value('date')


  @property
  def signed_by_author(self):
    return self.get_value('signed_by_author')


  @property
  def content_element(self):
    return self.get_one('content')


  def validate_format(self):
    names = sorted(self.element_children_names)
    expected = 'title author_name date signed_by_author content'
    expected = sorted(expected.split())
    if names != expected:
      msg = "Found these child elements: "
      msg += ''.join(['\n- ' + x for x in names])
      msg += '\nBut expected these child elements:'
      msg += ''.join(['\n- ' + x for x in expected])
      raise ValueError(msg)
    v.validate_title(self.title, article_type='article')
    v.validate_author_name(self.author_name)
    v.validate_date(self.date)
    v.validate_signed_by_author(self.signed_by_author)


  def set_file_path(self, file_path):
    v.validate_string(file_path)
    self.file_path = file_path
    self.file_name = os.path.basename(file_path)


  def validate_file_name(self):
    v.validate_article_file_name(
      self.file_name,
      self.date,
      self.author_name,
      self.uri_title,
    )
