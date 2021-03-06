# Imports
import logging




# Relative imports
from . import edgecase_article




# ### Notes
# Importing a package essentially imports the package's __init__.py file as a module.




# Collect up the things that we want in the immediate namespace of the imported datajack module.
# This file allows a script placed just above this package to run this:
# import edgecase_article
# edgecase_article.hello()
hello = edgecase_article.code.hello.hello
validate = edgecase_article.util.validate
configure_module_logger = edgecase_article.util.module_logger.configure_module_logger
#submodules = edgecase_article.submodules
keys = edgecase_article.code.keys
verify = edgecase_article.code.verify.verify
uri_title = edgecase_article.util.misc.uri_title
Article = edgecase_article.code.Article.Article
SignedArticle = edgecase_article.code.SignedArticle.SignedArticle
CheckpointArticle = edgecase_article.code.CheckpointArticle.CheckpointArticle
DatafeedArticle = edgecase_article.code.DatafeedArticle.DatafeedArticle
SignedDatafeedArticle = edgecase_article.code.SignedDatafeedArticle.SignedDatafeedArticle




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
  edgecase_article.util.module_logger.configure_module_logger(
    logger = logger,
    logger_name = __name__,
    log_level = log_level,
    debug = debug,
    log_timestamp = log_timestamp,
    log_file = log_file,
  )
  deb('Setup complete.')
  # Configure modules further down in this package.
  edgecase_article.setup(
    log_level = log_level,
    debug = debug,
    log_timestamp = log_timestamp,
    log_file = log_file,
  )
