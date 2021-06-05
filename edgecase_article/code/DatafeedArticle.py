# Imports
import os
import logging




# Relative imports
from .. import util
from .. import submodules
from . import Article
from . import SignedArticle
from . import CheckpointArticle




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




class DatafeedArticle(datajack.Element):


  @classmethod
  def from_element(cls, element):
    e = element
    e.__class__ = DatafeedArticle
    # Confirm that this DatafeedArticle contains exactly one of the following:
    # [checkpoint_article, signed_article, article]
    possibles = 'checkpoint_article signed_article article'.split()
    names = e.element_children_names
    found = [x for x in possibles if x in names]
    if len(found) != 1:
      raise ValueError
    e.child_article_type = found[0]
    e2 = e.get_one(e.child_article_type)
    # Choose child article's class based on its type.
    if e.child_article_type == 'article':
      e.article = Article.Article.from_element(e2)
    elif e.child_article_type == 'signed_article':
      e.article = SignedArticle.SignedArticle.from_element(e2)
    elif e.child_article_type == 'checkpoint_article':
      e.article = CheckpointArticle.CheckpointArticle.from_element(e2)
    e.article_type = 'datafeed_article'
    e.file_path = None
    e.file_name = None
    e.validate_format()
    return e


  def __str__(self):
    return 'DatafeedArticle: [{t}]'.format(t=self.title)


  @property
  def datafeed_name(self):
    return self.get_value('datafeed_name')


  @property
  def datafeed_article_id(self):
    return self.get_value('datafeed_article_id')


  @property
  def daid(self):
    return self.datafeed_article_id


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
    return self.get_branch_value('date').strip()


  @property
  def previous_checkpoint(self):
    if self.datafeed_article_id == '0':
      return None
    # Children of previous_checkpoint:
    # datafeed_article_id, checkpoint_id, date, transaction.
    # Children of previous_checkpoint/transaction:
    # blockchain_name, transaction_id, block_height,
    # source_address, destination_address
    return self.get_one('previous_checkpoint')


  @property
  def content_element(self):
    return self.article.content_element


  def validate_format(self):
    names = sorted(self.element_children_names)
    expected = 'datafeed_name datafeed_article_id date previous_checkpoint'
    expected += ' ' + self.child_article_type
    expected = sorted(expected.split())

    def error_msg(names, expected):
      msg = "Found these child elements: "
      msg += ''.join(['\n- ' + x for x in names])
      msg += '\nBut expected these child elements:'
      msg += ''.join(['\n- ' + x for x in expected])
      return msg

    if names != expected:
      raise ValueError(error_msg(names, expected))
    v.validate_datafeed_name(self.datafeed_name)
    v.validate_string_is_whole_number(self.datafeed_article_id)
    v.validate_date(self.date)
    # Look at previous_checkpoint child.
    if self.datafeed_article_id != '0':  # first checkpoint.
      pc_e = self.get_one('previous_checkpoint')
      pc_daid = pc_e.get_value('datafeed_article_id')
      v.validate_string_is_whole_number(pc_daid)
      pc_cid = pc_e.get_value('checkpoint_id')
      v.validate_string_is_whole_number(pc_cid)
      pc_date = pc_e.get_value('date')
      v.validate_date(pc_date)
      # Look at previous_checkpoint/transaction descendant.
      t_e = self.get_one('previous_checkpoint/transaction')
      t_txid = t_e.get_value('transaction_id')
      v.validate_hex_length(t_txid, 32)
      t_block_height = t_e.get_value('block_height')
      v.validate_string_is_whole_number(t_block_height)
      t_sa = t_e.get_all('source_address')
      t_da = t_e.get_all('destination_address')
      # Future: Verify the source address(es) and destination address(es).


  def set_file_path(self, file_path):
    v.validate_string(file_path)
    self.file_path = file_path
    file_name = os.path.basename(file_path)
    self.file_name = file_name


  def validate_file_name(self):
    v.validate_datafeed_article_file_name(
      self.file_name,
      self.date,
      self.article,
    )
