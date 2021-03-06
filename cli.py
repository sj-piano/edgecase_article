#!/usr/bin/python3




# Imports
import os
import sys
import argparse
import logging
import json




# Local imports
# (Can't use relative imports because this is a top-level script)
import edgecase_article




# Shortcuts
join = os.path.join
isfile = os.path.isfile
isdir = os.path.isdir
datajack = edgecase_article.submodules.datajack
stateless_gpg = edgecase_article.submodules.stateless_gpg
gpg = stateless_gpg.gpg
util = edgecase_article.util




# Notes:
# - Using keyword function arguments, each of which is on its own line,
# makes Python code easier to maintain. Arguments can be changed and
# rearranged much more easily.
# - I use "validate" to mean "check that this data is in the expected format".
# - I use "verify" to mean that "check that a mathematical operation produces the expected result". Example: Check a digital signature.
# - An article and the corresponding signed article have the same filenames. To distinguish between them, a newly created signed article should be saved in a different directory.
# - If the --verifyAssets option is used, this tool will look in the article directory for:
# 1) A directory named "assets"
# 2) A directory with the same name as the article, minus the .txt extension.




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
  logger_name = 'cli'
  # Configure logger for this module.
  edgecase_article.util.module_logger.configure_module_logger(
    logger = logger,
    logger_name = logger_name,
    log_level = log_level,
    debug = debug,
    log_timestamp = log_timestamp,
    log_file = log_file,
  )
  deb('Setup complete.')
  # Configure logging levels for edgecase_article package.
  # By default, without setup, it logs at ERROR level.
  # Optionally, the package could be configured here to use a different log level, by e.g. passing in 'error' instead of log_level.
  edgecase_article.setup(
    log_level = log_level,
    debug = debug,
    log_timestamp = log_timestamp,
    log_file = log_file,
  )




def main():

  # Note: We use camelCase for option names because it's faster to type.

  parser = argparse.ArgumentParser(
    description='Command-Line Interface (CLI) for using the edgecase_article package.'
  )

  parser.add_argument(
    '-t', '--task',
    help="Task to perform (default: '%(default)s').",
    default='hello',
  )

  parser.add_argument(
    '-a', '--articleType', dest='article_type',
    help="Type of article (default: '%(default)s').",
    default='unspecified',
  )

  parser.add_argument(
    '-f', '--articleFile', dest='article_file',
    help="Path to article file (default: '%(default)s').",
    default='new_articles/article.txt',
  )

  # Technically, this should be "validateFileName", but it seems more user-friendly to always use "verify" in the options.
  parser.add_argument(
    '-n', '--verifyFileName', dest='verify_file_name',
    action='store_true',
    help="Checks that the article's filename is in the proper format.",
  )

  parser.add_argument(
    '-v', '--verifySignature', dest='verify_signature',
    action='store_true',
    help="Checks that the article's signature(s) are valid.",
  )

  parser.add_argument(
    '-c', '--verifyContent', dest='verify_content',
    action='store_true',
    help="Validates the content element within an article.",
  )

  parser.add_argument(
    '-e', '--verifyAssets', dest='verify_assets',
    action='store_true',
    help="Validates that the assets in the assets directory match the asset links within the article.",
  )

  parser.add_argument(
    '--assetDir', dest='asset_dir',
    help="Path to directory containing assets of this article (default: '%(default)s'). If not supplied, the article path (minus the .txt extension) is used.",
    default=None,
  )

  parser.add_argument(
    '--publicKeyDir', dest='public_key_dir',
    help="Path to directory containing public keys (default: '%(default)s').",
    default=None,
  )

  parser.add_argument(
    '--privateKeyDir', dest='private_key_dir',
    help="Path to directory containing private keys (default: '%(default)s').",
    default=None,
  )

  parser.add_argument(
    '--deletedAssetsFile', dest='deleted_assets_file',
    help="Path to file containing information about deleted assets (default: '%(default)s').",
    default=None,
  )

  link_type_choices = 'hyperlink asset article external_asset'.split()
  parser.add_argument(
    '--linkType', dest='link_type',
    help="The type of link to generate (default: '%(default)s').",
    choices=link_type_choices,
    default=None,
  )

  parser.add_argument(
    '--articleLinksFile', dest='article_links_file',
    help="Path to file containing datafeed article links in JSON format (default: '%(default)s').",
    default='settings/datafeed_article_links.json',
  )

  parser.add_argument(
    '--assetLinksFile', dest='asset_links_file',
    help="Path to file containing datafeed asset links in JSON format (default: '%(default)s').",
    default='settings/datafeed_asset_links.json',
  )

  parser.add_argument(
    '-o', '--outputDir', dest='output_dir',
    help="Specify an output directory. (default: '%(default)s').",
    default='cli_output',
  )

  parser.add_argument(
    '-l', '--logLevel', type=str, dest='log_level',
    choices=['debug', 'info', 'warning', 'error'],
    help="Choose logging level (default: '%(default)s').",
    default='error',
  )

  parser.add_argument(
    '-d', '--debug',
    action='store_true',
    help="Sets logLevel to 'debug'. This overrides --logLevel.",
  )

  parser.add_argument(
    '-s', '--logTimestamp', dest='log_timestamp',
    action='store_true',
    help="Choose whether to prepend a timestamp to each log line.",
  )

  parser.add_argument(
    '-x', '--logToFile', dest='log_to_file',
    action='store_true',
    help="Choose whether to save log output to a file.",
  )

  parser.add_argument(
    '-z', '--logFile', dest='log_file',
    help="The path to the file that log output will be written to.",
    default='log_edgecase_article.txt',
  )

  a = parser.parse_args()

  # Check and analyse arguments
  if not a.log_to_file:
    a.log_file = None
  if not isfile(a.article_file):
    msg = "File not found at article_file {}".format(repr(a.article_file))
    raise FileNotFoundError(msg)
  if a.verify_signature:
    if not a.public_key_dir:
      msg = "To use verifySignature, need to specify a publicKeyDir."
      raise ValueError(msg)
    if not isdir(a.public_key_dir):
      msg = "Directory not found at publicKeyDir {}".format(repr(a.public_key_dir))
      raise FileNotFoundError(msg)
  if a.task == 'sign':
    if not a.public_key_dir:
      msg = "To use the 'sign' task, need to specify a publicKeyDir."
      raise ValueError(msg)
    if not isdir(a.public_key_dir):
      msg = "Directory not found at publicKeyDir {}".format(repr(a.public_key_dir))
    if not a.private_key_dir:
      msg = "To use the 'sign' task, need to specify a privateKeyDir."
      raise ValueError(msg)
    if not isdir(a.private_key_dir):
      msg = "Directory not found at privateKeyDir {}".format(repr(a.private_key_dir))
      raise FileNotFoundError(msg)
  if a.verify_assets:
    if not util.misc.shell_tool_exists('shasum'):
      msg = "Could not find shell tool 'shasum' on system."
      raise ValueError(msg)
    if a.deleted_assets_file:
      if not isfile(a.deleted_assets_file):
        msg = "File not found at deletedAssetsFile {}".format(repr(a.deleted_assets_file))
        raise FileNotFoundError(msg)
  if a.task == 'links':
    if not a.link_type:
      msg = "For task 'links', must choose a linkType."
      msg += '\nChoices: {}'.format(link_type_choices)
      raise ValueError(msg)
    if a.link_type == 'asset':
      if not a.asset_dir:
        msg = "For task 'links', with linkType='asset', must specify the assetDir."
        raise ValueError(msg)
    elif a.link_type == 'article':
      if not isfile(a.article_links_file):
        msg = "File not found at articleLinksFile {}"
        msg = msg.format(repr(a.article_links_file))
        raise FileNotFoundError(msg)
    elif a.link_type == 'external_asset':
      if not isfile(a.asset_links_file):
        msg = "File not found at assetLinksFile {}"
        msg = msg.format(repr(a.asset_links_file))
        raise FileNotFoundError(msg)

  # Setup
  setup(
    log_level = a.log_level,
    debug = a.debug,
    log_timestamp = a.log_timestamp,
    log_file = a.log_file,
  )

  # Create output directory.
  if a.task in 'links'.split():
    if not isdir(a.output_dir):
      os.makedirs(a.output_dir)
      msg = "Directory created: {}".format(a.output_dir)
      log(msg)

  # Run top-level function (i.e. the appropriate task).
  tasks = """
hello hello2 hello3 hello4 hello5
verify sign links
test
deriveURITitle constructFilename
""".split()
  if a.task not in tasks:
    msg = "Unrecognised task: {}".format(a.task)
    msg += "\nTask list: {}".format(tasks)
    stop(msg)
  globals()[a.task](a)  # run task.




def hello(a):
  # Confirm:
  # - that we can run a simple task.
  # - that this tool has working logging.
  log('Log statement at INFO level')
  deb('Log statement at DEBUG level')
  print('hello world')




def hello2(a):
  # Confirm:
  # - that we can run a simple task from within the package.
  # - that the package has working logging.
  edgecase_article.code.hello.hello()




def hello3(a):
  # Confirm:
  # - that we can run a simple package task that loads a resource file.
  edgecase_article.code.hello.hello_resource()




def hello4(a):
  # Confirm:
  # - that the datajack submodule can be accessed.
  e = datajack.Element()
  value = e.hello()
  print(value)




def hello5(a):
  # Confirm:
  # - that we can use the stateless_gpg submodule
  data = "hello world\n"
  log("data = " + data.strip())
  data_dir = 'edgecase_article/submodules/stateless_gpg/stateless_gpg/data'
  private_key_file = data_dir + '/test_key_1_private_key.txt'
  private_key = open(private_key_file).read()
  signature = gpg.make_signature(private_key, data)
  public_key_file = data_dir + '/test_key_1_public_key.txt'
  public_key = open(public_key_file).read()
  result = gpg.verify_signature(public_key, data, signature)
  log("result = " + str(result))
  if not result:
    raise Exception("Failed to create and verify signature.")
  print("Signature created and verified.")




def verify(a):
  # Load data from a.deleted_assets_file if it has been supplied.
  deleted_assets_element = None
  if a.deleted_assets_file:
    deleted_assets_data = open(a.deleted_assets_file).read().strip()
    deleted_assets_element = datajack.Element.from_string(deleted_assets_data)
  article = edgecase_article.code.verify.verify(
    article_file = a.article_file,
    article_type = a.article_type,
    verify_file_name = a.verify_file_name,
    verify_signature = a.verify_signature,
    verify_content = a.verify_content,
    public_key_dir = a.public_key_dir,
    verify_assets = a.verify_assets,
    asset_dir = a.asset_dir,
    deleted_assets_element = deleted_assets_element,
  )
  msg = 'Article file {} loaded and verified.'.format(a.article_file)
  log(msg)




def sign(a):
  signed_article = edgecase_article.code.sign.sign(
    article_file = a.article_file,
    public_key_dir = a.public_key_dir,
    private_key_dir = a.private_key_dir,
  )
  print(signed_article.data)




def links(a):

  # Load article.
  article_data = open(a.article_file).read()

  asset_files = []
  if a.link_type == 'asset':
    # Load asset file names.
    asset_file_names = sorted(os.listdir(a.asset_dir))
    asset_files = [join(a.asset_dir, x) for x in asset_file_names]
    msg = "{} asset files found in asset directory {}"
    msg = msg.format(len(asset_files), a.asset_dir)
    log(msg)

  article_links = {}
  if a.link_type == 'article':
    # Load article links data.
    article_links = json.load(open(a.article_links_file))
    article_links = article_links['data'][0]['datafeed_article_links']

  asset_links = {}
  if a.link_type == 'external_asset':
    # Load asset links data.
    asset_links = json.load(open(a.asset_links_file))
    asset_links = asset_links['data'][0]['datafeed_asset_links']

  # Analyse article.
  results = edgecase_article.code.links.generate_or_select_links(
    article_data,
    a.link_type,
    asset_files,
    article_links,
    asset_links,
  )

  # Select output file.
  if a.link_type == 'hyperlink':
    output_file_name = 'generated_hyperlinks.txt'
    msg = "Generated EML hyperlinks written to {}"
  elif a.link_type == 'asset':
    output_file_name = 'generated_asset_links.txt'
    msg = "Generated EML asset links written to {}"
  elif a.link_type == 'article':
    output_file_name = 'selected_datafeed_article_links.txt'
    msg = "Selected EML article links written to {}"
  elif a.link_type == 'external_asset':
    output_file_name = 'selected_datafeed_asset_links.txt'
    msg = "Selected EML asset links written to {}"
  else:
    raise ValueError

  # Write result to output file.
  output_file = join(a.output_dir, output_file_name)
  with open(output_file, 'w') as f:
    for result in results:
      f.write(result + '\n\n')
  msg = msg.format(output_file)
  log(msg)

  # Print results.
  for result in results:
    print(result + '\n\n')




def test(a):
  article = edgecase_article.code.verify.verify(
    article_file = a.article_file,
    article_type = a.article_type,
    verify_file_name = a.verify_file_name,
    verify_signature = False,
    verify_content = False,
    public_key_dir = a.public_key_dir,
    asset_dir = a.asset_dir,
  )
  msg = 'Article file {} loaded and verified.'.format(a.article_file)
  log(msg)
  block_height = article.previous_checkpoint.get_value('transaction/block_height')
  print('block_height: ' + str(block_height))




def deriveURITitle(a):
  article = edgecase_article.code.verify.verify(
    article_file = a.article_file,
    article_type = a.article_type,
    verify_file_name = a.verify_file_name,
    verify_signature = False,
    verify_content = False,
    public_key_dir = a.public_key_dir,
    asset_dir = a.asset_dir,
  )
  print(article.uri_title)




def constructFilename(a):
  article = edgecase_article.code.verify.verify(
    article_file = a.article_file,
    article_type = a.article_type,
    verify_file_name = a.verify_file_name,
    verify_signature = False,
    verify_content = False,
    public_key_dir = a.public_key_dir,
    asset_dir = a.asset_dir,
  )
  print(article.construct_file_name())




def stop(msg=None):
  if msg is not None:
    print(msg)
  import sys
  sys.exit()




if __name__ == '__main__':
  main()
