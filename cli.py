#!/usr/bin/python3




# Imports
import os
import sys
import argparse
import logging




# Local imports
# (Can't use relative imports because this is a top-level script)
import edgecase_client




# Notes:
# - Using keyword function arguments, each of which is on its own line,
# makes Python code easier to maintain. Arguments can be changed and
# rearranged much more easily.




# Set up logger for this module. By default, it logs at ERROR level.
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
  edgecase_client.util.module_logger.configure_module_logger(
    logger = logger,
    logger_name = logger_name,
    log_level = log_level,
    debug = debug,
    log_timestamp = log_timestamp,
    log_filepath = log_filepath,
  )
  log('Setup complete.')
  deb('Logger is logging at debug level.')
  # Configure logging levels for edgecase_client package.
  # By default, without setup, it logs at ERROR level.
  # Optionally, the package could be configured here to use a different log level, by e.g. passing in 'error' instead of log_level.
  edgecase_client.setup(
    log_level = log_level,
    debug = debug,
    log_timestamp = log_timestamp,
    log_filepath = log_filepath,
  )




def main():

  # Note: We use camelCase for option names because it's faster to type.

  parser = argparse.ArgumentParser(
    description='Command-Line Interface (CLI) for using the datajack package.'
  )

  parser.add_argument(
    '-t', '--task',
    help="Task to perform (default: '%(default)s').",
    default='hello',
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
    '-o', '--logToFile',
    action='store_true',
    help="Choose whether to save log output to a file.",
  )

  parser.add_argument(
    '-p', '--logFilepath',
    help="The path to the file that log output will be written to.",
    default='log_edgecase_client.txt',
  )

  a = parser.parse_args()

  log_filepath = a.logFilepath if a.logToFile else None

  # Setup
  setup(
    log_level = a.logLevel,
    debug = a.debug,
    log_timestamp = a.logTimestamp,
    log_filepath = log_filepath,
  )

  # Run top-level function (i.e. the appropriate task).
  tasks = 'hello hello2 hello3 hello4'.split()
  if a.task not in tasks:
    print("Unrecognised task: {}".format(a.task))
    stop()
  globals()[a.task](a)  # run task.




def hello(a):
  # Confirm:
  # - that we can run a simple task.
  # - that this tool has working logging.
  print('hello world')
  log('Log statement at INFO level')
  deb('Log statement at DEBUG level')




def hello2(a):
  # Confirm:
  # - that we can run a simple task from within the package.
  # - that the package has working logging.
  edgecase_client.code.hello.hello()




def hello3(a):
  # Confirm:
  # - that we can run a simple package task that loads a resource file.
  edgecase_client.code.hello.hello_resource()




def hello4(a):
  # Confirm:
  # - that a submodule can be accessed.
  e = edgecase_client.submodules.datajack.Element()
  print(e.hello())




def stop(msg=None):
  if msg is not None:
    print(msg)
  import sys
  sys.exit()




if __name__ == '__main__':
  main()
