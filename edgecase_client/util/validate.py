# Imports
import os
import string
import re




# Notes:
# - We treat this module as foundational. It shouldn't import anything other than standard library modules.
# - Functions at the bottom are the most basic.
# -- Functions further up may use functions below them.




# ### SECTION
# Components.

# https://stackoverflow.com/a/45598540
date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
hex_digits = '0123456789abcdef'


def build_error_msg(msg, value, name=None, location=None, kind=None):
  # Build out an expanded error message with useful detail.
  m = ''
  if location is not None:
    m += "in location {}, ".format(repr(location))
  if name is not None:
    # This is a complicated way of putting single quotes around _only_ the first word in the name.
    # This means that a description can be added after the name.
    words = name.split(' ')
    name2 = "'{}'".format(words[0])
    if len(words) > 1:
      name2 += ' ' + ' '.join(words[1:])
    m += "for variable {}, ".format(name2)
  if kind is not None:
    m += "expected a {}, but ".format(repr(kind))
  m += "received value {}".format(repr(value))
  if msg != '':
    m += ', ' + msg
  m = m[0].capitalize() + m[1:]
  return m




# ### SECTION
# Article property validation functions.




def validate_datafeed_article_file_name(file_name):
  # Example:
  # 2021-04-12_edgecase_datafeed_article_216_2021-04-12_stjohn_piano_discussion_crypto_messaging_apps.txt
  pass




def validate_article_file_name(
    file_name = None,
    date = None,
    author_name = None,
    uri_title = None,
    ):
  # Example:
  # 2019-04-14_stjohn_piano_a_simple_api__json_input_output.txt
  validate_date(date)
  validate_author_name(author_name)
  validate_uri_title(uri_title)
  file_name, ext = os.path.splitext(file_name)
  if ext != '.txt':
    raise ValueError
  d = file_name[:10]
  validate_date(d)
  if d != date:
    msg = "Date in filename ({}) differs from date in article ({}).".format(d, date)
    raise ValueError(msg)
  if file_name[10] != '_':
    raise ValueError
  n = len(author_name)
  an = file_name[11:11+n]
  if an != author_name:
    raise ValueError
  i = 11+n
  if file_name[i] != '_':
    msg = 'Char between author_name and uri_title (index {i}, in this case) must be an underscore. Instead, it is {c}.'.format(i=i, c=file_name[i])
    raise ValueError(msg)
  remaining = file_name[i+1:]
  if uri_title != remaining:
    msg = "Remaining portion of file_name ({r}) is not the same as the uri_title ({u})".format(r=remaining, u=uri_title)
    raise ValueError(msg)




def validate_signed_by_author(s):
  permitted = 'no yes'.split()
  if s not in permitted:
    raise ValueError




def validate_date(d):
  # Example: 2017-06-28
  if len(d) != 10:
    msg = 'Date ({}) must be exactly 10 characters.'.format(repr(d))
    raise ValueError(msg)
  for i in [4, 7]:
    if d[i] != '-':
      msg = "Char {i} [{c}] in date {d} must be '-'.".format(i=i, c=d[i], d=repr(d))
      raise ValueError(msg)
  d2 = d[:4] + d[5:7] + d[8:]
  if not d2.isdigit():
    msg = 'Date ({}), with hyphens removed, must contain only digits.'.format(repr(d))
    raise ValueError(msg)




def validate_author_name(n):
  # Example: stjohn_piano
  permitted = string.ascii_lowercase + '_'
  for c in n:
    if c not in permitted:
      msg = 'Character [{}] not permitted in article author_name.'.format(repr(c))
      raise ValueError(msg)




def validate_uri_title(u):
  # Examples:
  # stalky__co__by_rudyard_kipling_in_ambush
  # recipe_for_installing_kafka_2_5_0_as_a_systemd_service_on_ubuntu_16_04
  permitted = string.ascii_lowercase + '_'
  for c in u:
    if c not in permitted:
      msg = 'Character [{}] not permitted in uri_title.'.format(repr(c))
      raise ValueError(msg)




def validate_title(t, article_type):
  if article_type == 'checkpoint_article':
    # Example: checkpoint_0
    if t[:10] != 'checkpoint':
      raise ValueError
    if t[10] != '_':
      raise ValueError
    if not t[11:].isdigit():
      raise ValueError
  else:
    # Example: Discussion:_Crypto_Messaging_Apps
    if t[0] not in string.ascii_uppercase:
      raise ValueError('First character must be uppercase')
    permitted = string.ascii_letters + string.digits + "#&'(),-./:_" + '"'
    for c in t:
      if c not in permitted:
        msg = 'Character [{}] not permitted in article title.'.format(repr(c))
        raise ValueError(msg)




def validate_article_type(article_type, name=None, location=None, kind='article_type'):
  article_types = """
article signed_article checkpoint_article
datafeed_article signed_datafeed_article
""".split()
  if article_type not in article_types:
    msg = "Unrecognised article_type: {}".format(article_type)
    raise ValueError(msg)








# ### SECTION
# Basic validation functions.




def validate_whole_number(n, name=None, location=None, kind='whole_number'):
  # 0 is a whole number.
  if n == 0:
    return
  validate_positive_integer(n, name, location, kind)


wn = validate_whole_number


def validate_positive_integer(n, name=None, location=None, kind='positive_integer'):
  validate_integer(n, name, location, kind)
  if n < 0:
    msg = "which is less than 0."
    msg = build_error_msg(msg, n, name, location, kind)
    raise ValueError(msg)


pi = validate_positive_integer


def validate_integer(n, name=None, location=None, kind='integer'):
  if not isinstance(n, int):
    msg = "which has type '{}', not 'int'.".format(type(n).__name__)
    msg = build_error_msg(msg, n, name, location, kind)
    raise TypeError(msg)


i = validate_integer


def validate_boolean(b, name=None, location=None, kind='boolean'):
  if type(b) != bool:
    msg = "which has type '{}', not 'bool'.".format(type(b).__name__)
    msg = build_error_msg(msg, b, name, location, kind)
    raise TypeError(msg)


b = validate_boolean


def validate_hex_length(s, n, name=None, location=None, kind=None):
  if kind is None:
    kind = 'hex_length_{}_bytes'.format(n)
  validate_hex(s, name, location, kind)
  if not isinstance(n, int):
    msg = "which has type '{}', not 'int'.".format(type(n).__name__)
    name2 = 'n (i.e. the hex length)'
    msg = build_error_msg(msg, n, name=name2, location=location, kind=None)
    raise TypeError(msg)
  # 1 byte is 2 hex chars.
  if len(s) != n * 2:
    msg = "whose length is {} chars, not {} chars.".format(len(s), n * 2)
    msg = build_error_msg(msg, s, name, location, kind)
    raise ValueError(msg)


def validate_hex(s, name=None, location=None, kind='hex'):
  validate_string(s, name, location, kind)
  # find indices of non-hex characters in the string.
  indices = [i for i in range(len(s)) if s[i] not in hex_digits]
  if len(indices) > 0:
    non_hex_chars = [s[i] for i in indices]
    msg = "where the chars at indices {} (with values {}) are not hex chars.".format(indices, ','.join(non_hex_chars))
    msg = build_error_msg(msg, s, name, location, kind)
    raise ValueError(msg)


def validate_string_is_decimal(
    s, dp=2, name=None, location=None, kind='integer',
    ):
  # dp = decimal places
  string(s, name, location, kind)
  if not isinstance(dp, int):
    msg = "which has type '{}', not 'int'.".format(type(dp).__name__)
    name2 = 'dp (i.e. the number of decimal places)'
    msg = build_error_msg(msg, dp, name=name2, location=location, kind=None)
    raise TypeError(msg)
  regex = r'^\d*.\d{%d}$' % dp
  decimal_pattern = re.compile(regex)
  if not decimal_pattern.match(s):
    msg = 'which is not a valid {}-decimal-place decimal value.'.format(dp)
    msg = build_error_msg(msg, s, name, location, kind)
    raise ValueError(msg)


sd = validate_string_is_decimal


def validate_string_is_whole_number(
    s, name=None, location=None, kind='string_is_whole_number',
    ):
  # 0 is a whole number.
  validate_string(s, name, location, kind)
  if s == '0':
    return
  validate_string_is_positive_integer(s, name, location, kind)


swn = validate_string_is_whole_number


def validate_string_is_positive_integer(
    s, name=None, location=None, kind='string_is_positive_integer',
    ):
  validate_string(s, name, location, kind)
  if s == '0':
    raise ValueError('0 is not a positive number.')
  # find indices of non-digit characters in the string.
  indices = [i for i in range(len(s)) if not s[i].isdigit()]
  if len(indices) > 0:
    non_digit_chars = [s[i] for i in indices]
    msg = "where the chars at indices {} (with values {}) are not digits.".format(indices, ','.join(non_digit_chars))
    msg = build_error_msg(msg, s, name, non_digit_chars, kind)
    raise ValueError(msg)


spi = validate_string_is_positive_integer


def validate_string_is_date(s, name=None, location=None, kind='string_is_date'):
  validate_string(s, name, location, kind)
  if not date_pattern.match(s):
    msg = 'which is not a valid YYYY-MM-DD date string.'
    msg = build_error_msg(msg, s, name, location, kind)
    raise ValueError(msg)


sdate = validate_string_is_date


def validate_string(s, name=None, location=None, kind='string'):
  if not isinstance(s, str):
    msg = "which has type '{}', not 'str'.".format(type(s).__name__)
    msg = build_error_msg(msg, s, name, location, kind)
    raise TypeError(msg)


s = validate_string




