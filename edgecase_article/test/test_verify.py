# Imports
import os
import pytest
import pkgutil




# Relative imports
from .. import code
from .. import util
from .. import submodules




# Shortcuts
verify = code.verify.verify
join = os.path.join




# Setup for this file.
@pytest.fixture(autouse=True, scope='module')
def setup_module(pytestconfig):
  # If log_level is supplied to pytest in the commandline args, then use it to set up the logging in the application code.
  log_level = pytestconfig.getoption('log_cli_level')
  if log_level is not None:
    log_level = log_level.lower()
    code.setup(log_level = log_level)
    submodules.setup(log_level = log_level)




@pytest.fixture(autouse=True, scope='function')
def conf():
  # 'conf' = configuration
  conf = {}
  conf['data_dir'] = 'edgecase_article/data'
  conf['public_key_dir'] = 'edgecase_article/data/public_keys'
  conf['private_key_dir'] = 'edgecase_article/data/private_keys'
  return conf




# ### SECTION
# These tests are expected to work.


def test_verify_article(conf):
  article_name = 'article.txt'
  article_file = join(conf['data_dir'], article_name)
  article = verify(
    article_path = article_file,
    article_type = 'unspecified',
    verify_file_name = False,
    verify_signature = False,
    verify_content = True,
    public_key_dir = None,
  )
  assert article.title == 'Test_Article'
  assert article.author_name == 'test_key_1'


def test_verify_article_file_name(conf):
  article_name = '2021-05-05_test_key_1_test_article.txt'
  article_file = join(conf['data_dir'], article_name)
  article = verify(
    article_path = article_file,
    article_type = 'unspecified',
    verify_file_name = True,
    verify_signature = False,
    verify_content = True,
    public_key_dir = conf['public_key_dir'],
  )


def test_verify_signed_article(conf):
  article_name = '2021-05-05_test_key_1_test_article.txt.signed'
  article_file = join(conf['data_dir'], article_name)
  article = verify(
    article_path = article_file,
    article_type = 'signed_article',
    verify_file_name = False,
    verify_signature = True,
    verify_content = True,
    public_key_dir = conf['public_key_dir'],
  )
  assert article.title == 'Test_Article'
  assert article.author_name == 'test_key_1'


def test_verify_signed_article_2(conf):
  article_name = 'signed_article.txt'
  article_file = join(conf['data_dir'], article_name)
  article = verify(
    article_path = article_file,
    article_type = 'signed_article',
    verify_file_name = False,
    verify_signature = True,
    verify_content = True,
    public_key_dir = conf['public_key_dir'],
  )
  assert article.title == 'Test_Article'
  assert article.author_name == 'test_key_1'


def test_verify_signed_article_file_name(conf):
  article_name = '2017-06-28_stjohn_piano_viewpoint.txt'
  article_file = join(conf['data_dir'], article_name)
  article = verify(
    article_path = article_file,
    article_type = 'signed_article',
    verify_file_name = False,
    verify_signature = True,
    verify_content = True,
    public_key_dir = conf['public_key_dir'],
  )
  assert article.title == 'Viewpoint'
  assert article.author_name == 'stjohn_piano'


def test_verify_checkpoint_article(conf):
  article_name = 'checkpoint_article.txt'
  article_file = join(conf['data_dir'], article_name)
  article = verify(
    article_path = article_file,
    article_type = 'checkpoint_article',
    verify_file_name = False,
    verify_signature = False,
    verify_content = True,
    public_key_dir = None,
  )
  assert article.title == 'checkpoint_0'


def test_verify_checkpoint_article_file_name(conf):
  article_name = 'checkpoint_0.txt'
  article_file = join(conf['data_dir'], article_name)
  article = verify(
    article_path = article_file,
    article_type = 'unspecified',
    verify_file_name = True,
    verify_signature = False,
    verify_content = True,
    public_key_dir = None,
  )
  assert article.title == 'checkpoint_0'


def test_verify_datafeed_article_containing_article(conf):
  article_name = 'datafeed_article_containing_article.txt'
  article_file = join(conf['data_dir'], article_name)
  article = verify(
    article_path = article_file,
    article_type = 'unspecified',
    verify_file_name = False,
    verify_signature = False,
    verify_content = True,
    public_key_dir = None,
  )
  assert article.title == 'Discussion:_Crypto_Messaging_Apps'


def test_verify_datafeed_article_containing_article_file_name(conf):
  article_name = '2021-04-12_edgecase_datafeed_article_216_2021-04-12_stjohn_piano_discussion_crypto_messaging_apps.txt'
  article_file = join(conf['data_dir'], article_name)
  article = verify(
    article_path = article_file,
    article_type = 'unspecified',
    verify_file_name = True,
    verify_signature = False,
    verify_content = True,
    public_key_dir = None,
  )
  assert article.title == 'Discussion:_Crypto_Messaging_Apps'


def test_verify_datafeed_article_containing_signed_article(conf):
  article_name = 'datafeed_article_containing_signed_article.txt'
  article_file = join(conf['data_dir'], article_name)
  article = verify(
    article_path = article_file,
    article_type = 'unspecified',
    verify_file_name = False,
    verify_signature = False,
    verify_content = True,
    public_key_dir = None,
  )
  assert article.title == 'Viewpoint'


def test_verify_datafeed_article_containing_signed_article_file_name(conf):
  article_name = '2017-06-28_edgecase_datafeed_article_1_2017-06-28_stjohn_piano_viewpoint.txt'
  article_file = join(conf['data_dir'], article_name)
  article = verify(
    article_path = article_file,
    article_type = 'datafeed_article',
    verify_file_name = True,
    verify_signature = False,
    verify_content = True,
    public_key_dir = None,
  )
  assert article.title == 'Viewpoint'


def test_verify_datafeed_article_containing_checkpoint_article(conf):
  article_name = 'datafeed_article_containing_checkpoint_article.txt'
  article_file = join(conf['data_dir'], article_name)
  article = verify(
    article_path = article_file,
    article_type = 'unspecified',
    verify_file_name = False,
    verify_signature = False,
    verify_content = True,
    public_key_dir = None,
  )
  assert article.title == 'checkpoint_1'


def test_verify_datafeed_article_containing_checkpoint_article_file_name(conf):
  article_name = '2017-06-28_edgecase_datafeed_article_2_checkpoint_1.txt'
  article_file = join(conf['data_dir'], article_name)
  article = verify(
    article_path = article_file,
    article_type = 'unspecified',
    verify_file_name = True,
    verify_signature = False,
    verify_content = True,
    public_key_dir = None,
  )
  assert article.title == 'checkpoint_1'


def test_verify_signed_datafeed_article_containing_article(conf):
  # Bad sig
  article_name = 'signed_datafeed_article_containing_article.txt'
  article_file = join(conf['data_dir'], article_name)
  article = verify(
    article_path = article_file,
    article_type = 'unspecified',
    verify_file_name = False,
    verify_signature = True,
    verify_content = True,
    public_key_dir = conf['public_key_dir'],
  )
  assert article.title == 'Blockchain_Fundamentals'


def test_verify_signed_datafeed_article_containing_article_file_name(conf):
  # Bad sig
  article_name = '2019-04-21_edgecase_datafeed_article_104_2019-04-21_stjohn_piano_blockchain_fundamentals.txt'
  article_file = join(conf['data_dir'], article_name)
  article = verify(
    article_path = article_file,
    article_type = 'unspecified',
    verify_file_name = True,
    verify_signature = True,
    verify_content = True,
    public_key_dir = conf['public_key_dir'],
  )
  assert article.title == 'Blockchain_Fundamentals'


def test_verify_signed_datafeed_article_containing_signed_article(conf):
  article_name = 'signed_datafeed_article_containing_signed_article.txt'
  article_file = join(conf['data_dir'], article_name)
  article = verify(
    article_path = article_file,
    article_type = 'unspecified',
    verify_file_name = False,
    verify_signature = True,
    verify_content = True,
    public_key_dir = conf['public_key_dir'],
  )
  assert article.title == 'Blockchain_Fundamentals'


def test_verify_signed_datafeed_article_containing_signed_article_file_name(conf):
  article_name = '2019-04-21_edgecase_datafeed_article_104_2019-04-21_stjohn_piano_blockchain_fundamentals.txt'
  article_file = join(conf['data_dir'], article_name)
  article = verify(
    article_path = article_file,
    article_type = 'unspecified',
    verify_file_name = True,
    verify_signature = True,
    verify_content = True,
    public_key_dir = conf['public_key_dir'],
  )
  assert article.title == 'Blockchain_Fundamentals'


def test_verify_signed_datafeed_article_containing_checkpoint_article(conf):
  article_name = 'signed_datafeed_article_containing_checkpoint_article.txt'
  article_file = join(conf['data_dir'], article_name)
  article = verify(
    article_path = article_file,
    article_type = 'unspecified',
    verify_file_name = False,
    verify_signature = True,
    verify_content = True,
    public_key_dir = conf['public_key_dir'],
  )
  assert article.title == 'checkpoint_2'


def test_verify_signed_datafeed_article_containing_checkpoint_article_file_name(conf):
  article_name = '2017-07-13_edgecase_datafeed_article_4_checkpoint_2.txt'
  article_file = join(conf['data_dir'], article_name)
  article = verify(
    article_path = article_file,
    article_type = 'unspecified',
    verify_file_name = True,
    verify_signature = True,
    verify_content = True,
    public_key_dir = conf['public_key_dir'],
  )
  assert article.title == 'checkpoint_2'




# ### SECTION
# These tests are expected to fail.


def test_verify_signed_datafeed_article_bad_signature(conf):
  article_name = '2017-07-24_edgecase_datafeed_article_5_2017-07-21_stjohn_piano_james_sullivan_on_the_nature_of_banks.txt'
  article_file = join(conf['data_dir'], article_name)
  with pytest.raises(ValueError):
    article = verify(
      article_path = article_file,
      article_type = 'unspecified',
      verify_file_name = False,
      verify_signature = True,
      verify_content = False,
      public_key_dir = conf['public_key_dir'],
    )
