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




class CheckpointArticle(datajack.Element):


  @classmethod
  def from_element(cls, element):
    e = element
    e.__class__ = CheckpointArticle
    e.article_type = 'checkpoint_article'
    e.file_path = None
    e.file_name = None
    e.validate_format()
    return e


  def __str__(self):
    return 'CheckpointArticle: [{t}]'.format(t=self.title)


  @property
  def checkpoint_id(self):
    return self.get_value('checkpoint_id')


  @property
  def title(self):
    return self.get_value('title')


  @property
  def uri_title(self):
    return util.misc.uri_title(self.title)


  @property
  def author_name(self):
    return 'edgecase_datafeed'


  @property
  def date(self):
    return self.get_branch_value('date').strip()


  @property
  def blockchain_name(self):
    return self.get_value('block/blockchain_name')


  @property
  def block_height(self):
    return self.get_branch_value('block/block_height').strip()


  @property
  def content_element(self):
    return self.get_one('content')


  def validate_format(self):
    names = sorted(self.element_children_names)
    expected = 'checkpoint_id title date block content'
    expected = sorted(expected.split())
    if names != expected:
      msg = "Found these child elements: "
      msg += ''.join(['\n- ' + x for x in names])
      msg += '\nBut expected these child elements:'
      msg += ''.join(['\n- ' + x for x in expected])
      raise ValueError(msg)
    v.validate_string_is_whole_number(self.checkpoint_id)
    v.validate_title(self.title, article_type='checkpoint_article')
    v.validate_date(self.date)
    # Look at block child.
    block_e = self.get_one('block')
    names2 = sorted(block_e.element_children_names)
    expected2 = 'blockchain_name block_height'
    expected2 = sorted(expected2.split())
    if names2 != expected2:
      msg = "For child 'block', found these child elements: "
      msg += ''.join(['\n- ' + x for x in names2])
      msg += '\nBut expected these child elements:'
      msg += ''.join(['\n- ' + x for x in expected2])
      raise ValueError(msg)
    v.validate_blockchain_name(self.blockchain_name)
    v.validate_string_is_whole_number(self.block_height)


  def set_file_path(self, file_path):
    v.validate_string(file_path)
    self.file_path = file_path
    file_name = os.path.basename(file_path)
    self.file_name = file_name


  def validate_file_name(self):
    v.validate_checkpoint_article_file_name(
      self.file_name,
      self.uri_title,
    )
