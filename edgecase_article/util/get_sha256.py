# Imports
import os
import logging
import sys




# Relative imports.
from . import misc
from . import sha256




def get_sha256_of_file(file_path):
  # Calculate the SHA256 hash digest of a file using multiple implementations.
  # Avoid using Python SHA256 implementations if the file is > 1 MB in size.
  # We always use the shell SHA256 (perl underneath, I believe).
  cmd = 'shasum -a 256 {}'.format(file_path)
  output, exit_code = misc.run_local_cmd(cmd)
  sha256_shell = output.split(' ')[0]
  hashes = [sha256_shell]
  if os.path.getsize(file_path) < 10**6:
    # Note: Python 2 is called through the shell.
    asset_bytes = open(file_path, 'rb').read()
    sha256_py3 = sha256.SHA256(asset_bytes).hexdigest()
    hashes.append(sha256_py3)
    if misc.shell_tool_exists('python2'):
      sha256_py2 = misc.pypy_sha256(asset_bytes)
      hashes.append(sha256_py2)
  if len(set(hashes)) == 1:
    return hashes[0]
  raise ValueError
