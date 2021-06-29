#!/usr/bin/python2




# Goal: Provide a cmd-line tool that:
# - takes a filepath argument.
# - applies the PyPy SHA256 implementation to the data in the file.
# - prints the resulting hash digest in hex.




# Imports
import os
import argparse
import binascii




# Local imports
# (Can't use relative imports because this is a top-level script)
import pypy_sha256




# Shortcuts
isfile = os.path.isfile




def main():

  parser = argparse.ArgumentParser(
    description='Command-line tool for applying a Python2 SHA256 implementation to a file.'
  )

  parser.add_argument(
    '-f', '--targetFile', dest='target_file',
    help="Path to target file (default: '%(default)s').",
    default=None,
  )

  a = parser.parse_args()

  if a.target_file is None:
    msg = "targetFile argument not supplied."
    raise ValueError(msg)

  if not isfile(a.target_file):
    msg = "File not found at target_file {}".format(repr(a.target_file))
    raise FileNotFoundError(msg)

  # Load file.
  data = open(a.target_file).read()

  # Calculate SHA256 hash digest of file data.
  digest = sha256(data)
  print(digest)




def sha256(input_bytes):
  digest_bytes = pypy_sha256.sha256(input_bytes).digest()
  n = len(digest_bytes)
  if n != 32:
    msg = "Expected SHA256 result to be 32 bytes long."
    msg += "Instead, it was {} bytes.".format(n)
    raise ValueError(msg)
  digest_hex = binascii.hexlify(digest_bytes)
  return digest_hex




if __name__ == '__main__':
  main()
