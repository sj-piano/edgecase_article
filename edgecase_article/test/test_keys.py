# Imports
import pytest
import pkgutil




# Relative imports
from .. import code
from .. import util
from .. import submodules




# Setup for this file.
@pytest.fixture(autouse=True, scope='module')
def setup_module(pytestconfig):
  # If log_level is supplied to pytest in the commandline args, then use it to set up the logging in the application code.
  log_level = pytestconfig.getoption('log_cli_level')
  if log_level is not None:
    log_level = log_level.lower()
    code.setup(log_level = log_level)
    submodules.setup(log_level = log_level)








# ### SECTION


def test_strip_gpg_signature():
  signature = """
-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1

iQIcBAABAgAGBQJgjZPUAAoJEC8RP+HmG9MXI4IQAKEm82QBimrcQuvRS0UWdDXK
RPJKcjhf40ryHHC2w8vayLTE6Zev5EP5hOvQ7unOAEGOt4Es5fml4lbcPT792jRN
Ef12VFP1c+Uza7gYcz9SE0vrAra9J66uMeN2WOOUFw+l/Ig98KY14NnUNWZYUMGg
ZxzRKEKjNpTVvldX0/QEBc6NHbTsLmygwFjKvGN+1k4EWDd5ndGR7qCDncsG/lO+
bWuks/eClbEbZM56yN/XCBfQ+o+rZ0OExj2FFulKqZCpgy+n7IEim3VuTeXNs2fe
V1IPi9qOvY5f5KtKC4oEs6oQIm3Mbqy0TptU/dF3QQmcYIVRBQVzksj9amgID6d4
EKZtnvggO3Ozy18qh1l1YBVXzgcEcto3d/6tjh55GtPqkANkM1vs3K7PHPZjmflq
DwsTkit09C3s4j6ozFqA+68dlMOzlU4E2p69xzFAxACXr+FNgUG21RDvcq6UiXhf
r4Z0xvrmbeEyx3qkw9a2vsFfWiOijGcySn/y/A+Lf2a5fXQUqGqZvjC7VTpY6mxx
xdrmRo/EAsvOmW9R2SP1Rp+9YFImVWTm2ioZDhc1iiz2DcZ7mp2s1778oJmGw+as
sFnobxINks8Wbi9iq/tEWNHlLK4fNdiTsEA/g7vBgtskvd2vgwbvmrXxgillzchj
I/G56SIbDQx8QEavp9Eg
=H5CY
-----END PGP SIGNATURE-----
"""
  signature = signature.strip()
  expected = '\n'.join(signature.splitlines()[3:-1])
  result = code.keys.strip_gpg_signature(signature)
  assert result == expected


def test_strip_gpg_signature_2():
  # The version comment in the signature has been removed.
  signature = """
-----BEGIN PGP SIGNATURE-----

iQIcBAABAgAGBQJgjZPUAAoJEC8RP+HmG9MXI4IQAKEm82QBimrcQuvRS0UWdDXK
RPJKcjhf40ryHHC2w8vayLTE6Zev5EP5hOvQ7unOAEGOt4Es5fml4lbcPT792jRN
Ef12VFP1c+Uza7gYcz9SE0vrAra9J66uMeN2WOOUFw+l/Ig98KY14NnUNWZYUMGg
ZxzRKEKjNpTVvldX0/QEBc6NHbTsLmygwFjKvGN+1k4EWDd5ndGR7qCDncsG/lO+
bWuks/eClbEbZM56yN/XCBfQ+o+rZ0OExj2FFulKqZCpgy+n7IEim3VuTeXNs2fe
V1IPi9qOvY5f5KtKC4oEs6oQIm3Mbqy0TptU/dF3QQmcYIVRBQVzksj9amgID6d4
EKZtnvggO3Ozy18qh1l1YBVXzgcEcto3d/6tjh55GtPqkANkM1vs3K7PHPZjmflq
DwsTkit09C3s4j6ozFqA+68dlMOzlU4E2p69xzFAxACXr+FNgUG21RDvcq6UiXhf
r4Z0xvrmbeEyx3qkw9a2vsFfWiOijGcySn/y/A+Lf2a5fXQUqGqZvjC7VTpY6mxx
xdrmRo/EAsvOmW9R2SP1Rp+9YFImVWTm2ioZDhc1iiz2DcZ7mp2s1778oJmGw+as
sFnobxINks8Wbi9iq/tEWNHlLK4fNdiTsEA/g7vBgtskvd2vgwbvmrXxgillzchj
I/G56SIbDQx8QEavp9Eg
=H5CY
-----END PGP SIGNATURE-----
"""
  signature = signature.strip()
  expected = '\n'.join(signature.splitlines()[2:-1])
  result = code.keys.strip_gpg_signature(signature)
  assert result == expected
