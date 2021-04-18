# Importing a package essentially imports the package's __init__.py file as a module.
# This file allows a script placed just above this package to run this:
# import edgecase_client
# edgecase_client.edgecase_client.code.hello.hello()
from . import edgecase_client
