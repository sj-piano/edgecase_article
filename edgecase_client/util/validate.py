# Imports
import os
import string as string_module  # We have a function in here called 'string'.
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




def datafeed_article_file_name(s):
  # Example:
  # 2021-04-12_edgecase_datafeed_article_216_2021-04-12_stjohn_piano_discussion_crypto_messaging_apps.txt
  pass




def article_file_name(
    file_name = None,
    #article_date = None,
    #article_author_name = None,
    #article_title = None,
  ):
  # Example:
  # 2019-04-14_stjohn_piano_a_simple_api__json_input_output.txt
  file_name, ext = os.path.splitext(file_name)
  if ext != '.txt':
    raise ValueError
  d = file_name[:10]
  date(d)




def signed_by_author(s):
  permitted = 'no yes'.split()
  if s not in permitted:
    raise ValueError




def date(d):
  # Example: 2017-06-28
  if len(d) != 10:
    msg = 'Date [{}] must be exactly 10 characters.'.format(d)
    raise ValueError(msg)
  for i in [4,7]:
    if d[i] != '-':
      msg = 'Char {i} [{c}] in date [{d}] must be "-".'.format(i=i, c=d[i], d=d)
      raise ValueError(msg)
  d2 = d[:4] + d[5:7] + d[8:]
  if not d2.isdigit():
    msg = 'Date [{}] (with hyphens removed) must contain only digits.'.format(d)
    raise ValueError(msg)




def author_name(n):
  permitted = string_module.ascii_lowercase + '_'
  for c in n:
    if c not in permitted:
      msg = 'Character [{}] not permitted in article author_name.'.format(repr(c))
      raise ValueError(msg)




def title(t, article_type):
  if article_type == 'checkpoint_article':
    # Example: "checkpoint_0"
    if t[:10] != 'checkpoint':
      raise ValueError
    if t[10] != '_':
      raise ValueError
    if not t[11:].isdigit():
      raise ValueError
  else:
    # Example: Discussion:_Crypto_Messaging_Apps
    if t[0] not in string_module.ascii_uppercase:
      raise ValueError('First character must be uppercase')
    permitted = string_module.ascii_letters + string_module.digits + "#&'(),-./:_" + '"'
    for c in t:
      if c not in permitted:
        msg = 'Character [{}] not permitted in article title.'.format(repr(c))
        raise ValueError(msg)








# ### SECTION
# Basic validation functions.




def whole_number(n, name=None, location=None, kind='whole_number'):
  # 0 is a whole number.
  if n == 0:
    return
  positive_integer(n, name, location, kind)


wn = whole_number


def positive_integer(n, name=None, location=None, kind='positive_integer'):
  integer(n, name, location, kind)
  if n < 0:
    msg = "which is less than 0."
    msg = build_error_msg(msg, n, name, location, kind)
    raise ValueError(msg)


pi = positive_integer


def integer(n, name=None, location=None, kind='integer'):
  if not isinstance(n, int):
    msg = "which has type '{}', not 'int'.".format(type(n).__name__)
    msg = build_error_msg(msg, n, name, location, kind)
    raise TypeError(msg)


i = integer


def boolean(b, name=None, location=None, kind='boolean'):
  if type(b) != bool:
    msg = "which has type '{}', not 'bool'.".format(type(b).__name__)
    msg = build_error_msg(msg, b, name, location, kind)
    raise TypeError(msg)


b = boolean


def hex_length(s, n, name=None, location=None, kind=None):
  if kind is None:
    kind = 'hex_length_{}_bytes'.format(n)
  hex(s, name, location, kind)
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


def hex(s, name=None, location=None, kind='hex'):
  string(s, name, location, kind)
  # find indices of non-hex characters in the string.
  indices = [i for i in range(len(s)) if s[i] not in hex_digits]
  if len(indices) > 0:
    non_hex_chars = [s[i] for i in indices]
    msg = "where the chars at indices {} (with values {}) are not hex chars.".format(indices, ','.join(non_hex_chars))
    msg = build_error_msg(msg, s, name, location, kind)
    raise ValueError(msg)


def string_is_decimal(
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


sd = string_is_decimal


def string_is_whole_number(
    s, name=None, location=None, kind='string_is_whole_number',
    ):
  # 0 is a whole number.
  string(s, name, location, kind)
  if s == '0':
    return
  string_is_positive_integer(s, name, location, kind)


swn = string_is_whole_number


def string_is_positive_integer(
    s, name=None, location=None, kind='string_is_positive_integer',
    ):
  string(s, name, location, kind)
  if s == '0':
    raise ValueError('0 is not a positive number.')
  # find indices of non-digit characters in the string.
  indices = [i for i in range(len(s)) if not s[i].isdigit()]
  if len(indices) > 0:
    non_digit_chars = [s[i] for i in indices]
    msg = "where the chars at indices {} (with values {}) are not digits.".format(indices, ','.join(non_digit_chars))
    msg = build_error_msg(msg, s, name, non_digit_chars, kind)
    raise ValueError(msg)


spi = string_is_positive_integer


def string_is_date(s, name=None, location=None, kind='string_is_date'):
  string(s, name, location, kind)
  if not date_pattern.match(s):
    msg = 'which is not a valid YYYY-MM-DD date string.'
    msg = build_error_msg(msg, s, name, location, kind)
    raise ValueError(msg)


sdate = string_is_date


def string(s, name=None, location=None, kind='string'):
  if not isinstance(s, str):
    msg = "which has type '{}', not 'str'.".format(type(s).__name__)
    msg = build_error_msg(msg, s, name, location, kind)
    raise TypeError(msg)


s = string




