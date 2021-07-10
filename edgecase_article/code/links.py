# Imports
import os
import logging
import sys
import re




# Relative imports
from .. import util
from .. import submodules




# Shortcuts
v = util.validate
datajack = submodules.datajack
isdir = os.path.isdir
basename = os.path.basename
join = os.path.join




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




def generate_or_select_links(
    article_data = None,
    link_type = None,
    asset_files = None,
    article_links = None,
    asset_links = None,
    ):

  # Note: We always return a list.
  v.validate_string(article_data, 'article_data', 'links.py')
  v.validate_string(link_type, 'link_type', 'links.py')
  v.validate_list(asset_files, 'asset_files', 'links.py')
  v.validate_dict(article_links, 'article_links', 'links.py')
  v.validate_dict(asset_links, 'asset_links', 'links.py')


  if link_type == 'hyperlink':

    # Look through the article data for any hypertext links.
    pattern = r'http[s]?://[a-zA-Z0-9./_\-?=#~()+%:&]+'
    urls = re.findall(pattern, article_data)
    msg = "{} hyperlinks found.".format(len(urls))
    log(msg)
    # For each of these links, generate an equivalent EML hyperlink.
    template = """
<link>
<type>hyperlink</type>
<reference>{}</reference>
<text>{}</text>
</link>
  """.strip()
    hyperlinks = []
    for url in urls:
      reference = url
      text = url
      if text.startswith('https://'):
        text = text[len('https://'):]
      if text.startswith('http://'):
        text = text[len('http://'):]
      hyperlink = template.format(reference, text)
      hyperlinks.append(hyperlink)
    return hyperlinks


  elif link_type == 'asset':

    # For each asset file, generate an EML asset link.
    asset_links = []
    template = """
<link>
<type>asset</type>
<filename>{a}</filename>
<text>{a}</text>
<sha256>{h}</sha256>
</link>
""".strip()
    for asset_file in asset_files:
      asset_file_name = basename(asset_file)
      hash = util.get_sha256.get_sha256_of_file(asset_file)
      asset_link = template.format(a=asset_file_name, h=hash)
      asset_links.append(asset_link)
    return asset_links


  elif link_type == 'article':

    uri_title_to_article_link = {}
    for daid, article_link in article_links.items():
      article_link_element = datajack.Element.from_string(article_link)
      article_title = article_link_element.get_value('article_title')
      uri_title = util.misc.uri_title(article_title)
      uri_title_to_article_link[uri_title] = article_link

    # Look through the article data for any article link placeholders.
    # These contain article uri_titles.
    # Examples:
    # [LINK: excerpts_from_leviathan_wakes_by_james_s_a_corey]
    # [     LINK:blockchain_companies ]
    # [ LINK:blockchain_companies ]
    # [LINK: discussion_crypto_messaging_apps ]
    # [LINK:contract_1]
    # [LINK: monads_in_python]
    pattern = r'\[\s*LINK\s*:\s*(?P<placeholder>[a-z0-9_]*)\s*\]'
    placeholders = re.findall(pattern, article_data)
    msg = "{} article link placeholders found.".format(len(placeholders))
    log(msg)
    selected_links = []
    for placeholder in placeholders:
      if placeholder in uri_title_to_article_link.keys():
        article_link = uri_title_to_article_link[placeholder]
      else:
        article_link = "[no link found]"
      selected_link = placeholder + '\n' + article_link
      selected_links.append(selected_link)
    return selected_links


  elif link_type == 'external_asset':
    asset_filename_to_asset_link = {}
    for daid, links in asset_links.items():
      for link in links:
        link_element = datajack.Element.from_string(link)
        asset_filename = link_element.get_value('filename')
        asset_filename_to_asset_link[asset_filename] = link
    # Look through the article data for any asset link placeholders.
    # These contain the asset filename.
    # Examples:
    # [ASSET LINK: contract_1.txt]
    # [ ASSET LINK : the_eye_of_argon_by_jim_theis.pdf]
    pattern = r'\[\s*ASSET\s*LINK\s*:\s*(?P<placeholder>[a-z0-9_\-.]*)\s*\]'
    placeholders = re.findall(pattern, article_data)
    msg = "{} asset link placeholders found.".format(len(placeholders))
    log(msg)
    selected_links = []
    for placeholder in placeholders:
      if placeholder in asset_filename_to_asset_link.keys():
        asset_link = asset_filename_to_asset_link[placeholder]
      else:
        asset_link = "[no link found]"
      selected_link = placeholder + '\n' + asset_link
      selected_links.append(selected_link)
    return selected_links

  raise Exception




def stop(msg=None):
  if msg is not None:
    print(msg)
  import sys
  sys.exit()
