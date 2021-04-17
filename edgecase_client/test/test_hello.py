# Imports
import pytest
import pkgutil




# Relative imports
from .. import code
from .. import util




# Notes:
# - "work directory" = directory that contains this file.
# - Running the command { pytest3 edgecase_client/test/test_hello.py } in the work directory should load and run the tests in this file.
# - Run a specific test:
# -- pytest3 edgecase_client/test/test_hello.py::test_hello
# - Run quietly:
# -- pytest3 -q edgecase_client/test/test_hello.py
# - Print log data during a single test:
# -- pytest3 -o log_cli=true --log-cli-level=INFO --log-format="%(levelname)s [%(lineno)s: %(funcName)s] %(message)s" edgecase_client/test/test_hello.py::test_hello
# -- This is very useful when you want to manually check the operation of the functions during the test.
# Use the pytest -s option if you want print statements in the tests to actually print output.








# ### SECTION
# Basic checks.


def test_hello():
  x = 'hello'
  print(x)
  assert x == 'hello'


def test_hello_data():
  data_file = '../data/data1.txt'
  data = pkgutil.get_data(__name__, data_file).decode('ascii').strip()
  assert data == 'hello world'
