#!/usr/bin/python3




# Imports
import os
import sys
import argparse
import logging




# Local imports
# (Can't use relative imports because this is a top-level script)
import edgecase_article




# Shortcuts
isfile = os.path.isfile
isdir = os.path.isdir
datajack = edgecase_article.submodules.datajack
stateless_gpg = edgecase_article.submodules.stateless_gpg
gpg = stateless_gpg.gpg




# Notes:
# - Using keyword function arguments, each of which is on its own line,
# makes Python code easier to maintain. Arguments can be changed and
# rearranged much more easily.
# - I use "validate" to mean "check that this data is in the expected format".
# - I use "verify" to mean that "check that a mathematical operation produces the expected result". Example: Check a digital signature.




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
  logger_name = 'cli'
  # Configure logger for this module.
  edgecase_article.util.module_logger.configure_module_logger(
    logger = logger,
    logger_name = logger_name,
    log_level = log_level,
    debug = debug,
    log_timestamp = log_timestamp,
    log_filepath = log_filepath,
  )
  log('Setup complete.')
  deb('Logger is logging at debug level.')
  # Configure logging levels for edgecase_article package.
  # By default, without setup, it logs at ERROR level.
  # Optionally, the package could be configured here to use a different log level, by e.g. passing in 'error' instead of log_level.
  edgecase_article.setup(
    log_level = log_level,
    debug = debug,
    log_timestamp = log_timestamp,
    log_filepath = log_filepath,
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
    '-a', '--articleType',
    help="Type of article (default: '%(default)s').",
    default='unspecified',
  )

  parser.add_argument(
    '-p', '--articlePath',
    help="Path to article file (default: '%(default)s').",
    default='new_articles/signed_article.txt',
  )

  # Technically, this should be "validateFileName", but it seems more user-friendly to always use "verify" in the options.
  parser.add_argument(
    '-c', '--verifyFileName',
    action='store_true',
    help="Checks that the article's filename is in the proper format.",
  )

  parser.add_argument(
    '-v', '--verifySignature',
    action='store_true',
    help="Checks that the article's signature(s) are valid.",
  )

  parser.add_argument(
    '-k', '--publicKeyDir',
    help="Path to directory containing public keys (default: '%(default)s').",
    default=None,
  )

  parser.add_argument(
    '-q', '--privateKeyDir',
    help="Path to directory containing private keys (default: '%(default)s').",
    default=None,
  )

  parser.add_argument(
    '-l', '--logLevel', type=str,
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
    '-s', '--logTimestamp',
    action='store_true',
    help="Choose whether to prepend a timestamp to each log line.",
  )

  parser.add_argument(
    '-x', '--logToFile',
    action='store_true',
    help="Choose whether to save log output to a file.",
  )

  parser.add_argument(
    '-z', '--logFilepath',
    help="The path to the file that log output will be written to.",
    default='log_edgecase_article.txt',
  )

  a = parser.parse_args()

  log_filepath = a.logFilepath if a.logToFile else None

  # Check and analyse arguments
  if not isfile(a.articlePath):
    msg = "File not found at articlePath {}".format(repr(a.articlePath))
    raise FileNotFoundError(msg)
  if a.verifySignature:
    if a.publicKeyDir is None:
      msg = "To use verifySignature, need to specify a publicKeyDir."
      raise ValueError(msg)
    if not isdir(a.publicKeyDir):
      msg = "Directory not found at publicKeyDir {}".format(repr(a.publicKeyDir))
      raise FileNotFoundError(msg)

  # Setup
  setup(
    log_level = a.logLevel,
    debug = a.debug,
    log_timestamp = a.logTimestamp,
    log_filepath = log_filepath,
  )

  # Run top-level function (i.e. the appropriate task).
  tasks = """
hello hello2 hello3 hello4 hello5
verify
""".split()
  if a.task not in tasks:
    print("Unrecognised task: {}".format(a.task))
    stop()
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
  edgecase_article.code.verify.verify(
    article_path = a.articlePath,
    article_type = a.articleType,
    verify_file_name = a.verifyFileName,
    verify_signature = a.verifySignature,
    public_key_dir = a.publicKeyDir,
  )





def stop(msg=None):
  if msg is not None:
    print(msg)
  import sys
  sys.exit()




if __name__ == '__main__':
  main()
