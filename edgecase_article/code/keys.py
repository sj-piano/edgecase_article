# Imports
import os
import logging




# Relative imports
from .. import util




# Shortcuts
v = util.validate




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




def strip_gpg_signature(signature):
  # Remove the GPG wrapper text from the signature.
  # Example signature:
### BEGIN EXAMPLE
# -----BEGIN PGP SIGNATURE-----
# Version: GnuPG v1
#
# iQIcBAABAgAGBQJgjZPUAAoJEC8RP+HmG9MXI4IQAKEm82QBimrcQuvRS0UWdDXK
# RPJKcjhf40ryHHC2w8vayLTE6Zev5EP5hOvQ7unOAEGOt4Es5fml4lbcPT792jRN
# Ef12VFP1c+Uza7gYcz9SE0vrAra9J66uMeN2WOOUFw+l/Ig98KY14NnUNWZYUMGg
# ZxzRKEKjNpTVvldX0/QEBc6NHbTsLmygwFjKvGN+1k4EWDd5ndGR7qCDncsG/lO+
# bWuks/eClbEbZM56yN/XCBfQ+o+rZ0OExj2FFulKqZCpgy+n7IEim3VuTeXNs2fe
# V1IPi9qOvY5f5KtKC4oEs6oQIm3Mbqy0TptU/dF3QQmcYIVRBQVzksj9amgID6d4
# EKZtnvggO3Ozy18qh1l1YBVXzgcEcto3d/6tjh55GtPqkANkM1vs3K7PHPZjmflq
# DwsTkit09C3s4j6ozFqA+68dlMOzlU4E2p69xzFAxACXr+FNgUG21RDvcq6UiXhf
# r4Z0xvrmbeEyx3qkw9a2vsFfWiOijGcySn/y/A+Lf2a5fXQUqGqZvjC7VTpY6mxx
# xdrmRo/EAsvOmW9R2SP1Rp+9YFImVWTm2ioZDhc1iiz2DcZ7mp2s1778oJmGw+as
# sFnobxINks8Wbi9iq/tEWNHlLK4fNdiTsEA/g7vBgtskvd2vgwbvmrXxgillzchj
# I/G56SIbDQx8QEavp9Eg
# =H5CY
# -----END PGP SIGNATURE-----
### END EXAMPLE
  lines = signature.splitlines()
  if lines[0] != '-----BEGIN PGP SIGNATURE-----':
    raise ValueError
  # We expect a blank line prior to the signature data.
  # We'll extract the signature data starting at line 2.
  i = 2
  if lines[1] != '':
    # In this case, line 2 has a comment.
    # Example:
    # Version: GnuPG v1
    # We'll extract the signature data starting at line 3.
    if lines[2] != '':
      raise ValueError
    i = 3
  if lines[-1] != '-----END PGP SIGNATURE-----':
    raise ValueError
  extracted_lines = lines[i:-1]
  extraction = '\n'.join(extracted_lines)
  return extraction




def load_public_key(public_key_dir, author_name):
  # Example public key file name:
  # stjohn_piano_public_key.txt
  pk_ext = '_public_key.txt'
  items = os.listdir(public_key_dir)
  key_file_names = [x for x in items if os.path.splitext(x)[1] == '.txt']
  author_names = [x.replace(pk_ext, '') for x in key_file_names]
  if author_name not in author_names:
    msg = "Did not find any public key with author name {} in public key directory {}.".format(repr(author_name), repr(public_key_dir))
    raise FileNotFoundError(msg)
  key_file_name = author_name + pk_ext
  key_file = os.path.join(public_key_dir, key_file_name)
  public_key = open(key_file).read().strip()
  return public_key




def load_private_key(private_key_dir, author_name):
  # Example private key file name:
  # stjohn_piano_private_key.txt
  pk_ext = '_private_key.txt'
  items = os.listdir(private_key_dir)
  key_file_names = [x for x in items if os.path.splitext(x)[1] == '.txt']
  author_names = [x.replace(pk_ext, '') for x in key_file_names]
  if author_name not in author_names:
    msg = "Did not find any private key with author name {} in private key directory {}.".format(repr(author_name), repr(private_key_dir))
    raise FileNotFoundError(msg)
  key_file_name = author_name + pk_ext
  key_file = os.path.join(private_key_dir, key_file_name)
  private_key = open(key_file).read().strip()
  return private_key
