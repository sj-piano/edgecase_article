# Imports
import os
import pytest
import pkgutil




# Relative imports
from .. import code
from .. import util
from .. import submodules




# Shortcuts
sign = code.sign.sign
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


def test_sign_article(conf):
  article_name = '2021-05-09_test_key_1_test_article_2.txt'
  article_file = join(conf['data_dir'], article_name)
  signed_article = sign(
    article_path = article_file,
    public_key_dir = conf['public_key_dir'],
    private_key_dir = conf['private_key_dir'],
  )
  output_file = signed_article.file_path + '.signed'
  with open(output_file, 'w') as f:
    f.write(signed_article.data + '\n')
  signed_article2 = verify(
    article_path = output_file,
    article_type = 'signed_article',
    verify_file_name = False,  # It has the extra '.signed' extension.
    verify_signature = True,
    verify_content = True,
    public_key_dir = conf['public_key_dir'],
  )
  os.remove(output_file)
  assert signed_article2.title == 'Test_Article_2'
  assert signed_article2.author_name == 'test_key_1'
  assert signed_article2.date == '2021-05-09'
