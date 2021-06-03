# Imports
import os
import logging
import pkgutil
import sys
import traceback




# Relative imports
from .. import util
from .. import submodules
from . import Article
from . import SignedArticle
from . import CheckpointArticle
from . import DatafeedArticle
from . import SignedDatafeedArticle
from . import keys




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




def verify(
    article_file = None,
    article_type = None,
    verify_file_name = None,
    verify_signature = None,
    verify_content = None,
    public_key_dir = None,
    verify_assets = False,
    asset_dir = None,
    deleted_assets_element = None,
    ):
  v.validate_string(article_file)
  v.validate_string(article_type, 'article_type', 'verify.py')
  v.validate_boolean(verify_file_name)
  v.validate_boolean(verify_signature)
  v.validate_boolean(verify_content)
  v.validate_boolean(verify_assets)
  if article_type != 'unspecified':
    v.validate_article_type(article_type)
  try:
    e = datajack.Element.from_file(article_file)
  except Exception as ex:
    traceback.print_exception(type(ex), ex, ex.__traceback__)
    msg = "\nError summary: Unable to parse file into an EML Element."
    msg += "\n- File path: {}".format(article_file)
    stop(msg)
  msg = "File {} contains a valid Element.".format(article_file)
  log(msg)
  v.validate_article_type(e.name, 'e.name (element name)', 'verify.py')
  if article_type == 'unspecified':
    article_type = e.name
  if e.name != article_type:
      msg = "Expected article_type {}, found element with name {}.".format(
        repr(article_type), repr(e.name),
      )
      raise ValueError(msg)
  msg = "Element name: {}".format(e.name)
  log(msg)
  # Use the element name to select an article class.
  a = None
  if article_type == 'article':
    a = Article.Article.from_element(element=e)
  elif article_type == 'signed_article':
    a = SignedArticle.SignedArticle.from_element(element=e)
  elif article_type == 'checkpoint_article':
    a = CheckpointArticle.CheckpointArticle.from_element(element=e)
  elif article_type == 'datafeed_article':
    a = DatafeedArticle.DatafeedArticle.from_element(element=e)
  elif article_type == 'signed_datafeed_article':
    a = SignedDatafeedArticle.SignedDatafeedArticle.from_element(element=e)
  else:
    msg = "No class available for article_type {}".format(repr(article_type))
    raise ValueError(msg)
  a.set_file_path(article_file)
  if verify_file_name:
    a.validate_file_name()
    msg = "File name verified for {}".format(a.__class__.__name__)
    log(msg)
  if verify_signature:
    if a.article_type == 'signed_article':
      v.validate_string(public_key_dir)
      author_name = a.author_name
      public_key = keys.load_public_key(public_key_dir, author_name)
      a.verify_signature(public_key)
    elif a.article_type == 'signed_datafeed_article':
      v.validate_string(public_key_dir)
      datafeed_name = 'edgecase_datafeed'  # hardcoded.
      public_key = keys.load_public_key(public_key_dir, datafeed_name)
      a.verify_signature(public_key)
      # If it contains a signed article, then verify its signature also.
      if a.article.article_type == 'signed_article':
        author_name = a.article.author_name
        public_key2 = keys.load_public_key(public_key_dir, author_name)
        a.article.verify_signature(public_key2)
        msg = "Signature verified for internal {}".format(a.article.__class__.__name__)
        log(msg)
    else:
      msg = "verifySignature not possible for article_type {}".format(repr(a.article_type))
      raise ValueError(msg)
    msg = "Signature verified for {}".format(a.__class__.__name__)
    log(msg)
  if verify_content:
    # Load content settings.
    content_settings_file = '../../settings/content.txt'
    cs = pkgutil.get_data(__name__, content_settings_file)
    cs = cs.decode('ascii').strip()
    cs_e = datajack.Element.from_string(cs)
    permitted_names = cs_e.get_one('element_names').text
    permitted_names = permitted_names.strip().split('\n')
    if a.article_type in ['datafeed_article', 'signed_datafeed_article']:
      old_articles = cs_e.get('old_element_names/article[@id={}]'.format(a.daid))
      if len(old_articles) > 0:
        # This datafeed article contains some obsolete element names.
        old_names = old_articles[0].get_one('element_names').text
        old_names = old_names.strip().split('\n')
        permitted_names.extend(old_names)
    for d_e in a.content_element.element_descendants:
      if d_e.name not in permitted_names:
        msg = "Permitted names:"
        msg += ''.join(['\n- ' + str(x) for x in permitted_names])
        msg += "\nProblem: In 'content' element, found {} element".format(repr(d_e.name))
        msg += ", whose name does not appear in the list of permitted element names (shown above)."
        msg += "\n- Path from root element ({}):\n-- {}" \
          .format(a.name, repr(d_e.path_from_root))
        msg += "\n- Line {}, index {}".format(d_e.line_number, d_e.line_index)
        stop(msg)
    msg = "Content element: All descendant elements have permitted names."
    log(msg)
    # Some elements are required to have particular descendants.
    # We check their "trees".
    permitted_trees = cs_e.get_one('element_trees')
    z = '=' * 10  # z is a text divider
    for d_e in a.content_element.element_descendants:
      d_trees = permitted_trees.get(d_e.name)
      if len(d_trees) > 0:
        msg = "Examined element {}".format(repr(d_e.name))
        msg += ", with element tree:"
        msg += "\n" + z + "\n" + d_e.element_tree + "\n" + z
        msg += "\nChecked that it contained at least one of the following element trees, but it didn't:"
        success = False
        for tree in d_trees:
          msg += "\n" + z + "\n" + tree.element_tree + "\n" + z
          result, msg2 = d_e.contains_tree_of(tree)
          msg += msg2
          if result:
            success = True
        if not success:
          raise ValueError(msg)
    msg = "Content element: All descendant elements have been checked against the list of permitted tree structures."
    log(msg)
  if verify_assets:
    if not asset_dir:
      # Use the article_file, with the extension removed.
      asset_dir = os.path.splitext(article_file)[0]
    # Get list of asset links in article.
    asset_links = a.content_element.get("//link[@type='asset']")
    # Load types of asset link:
    text_asset_link_tree = """
<link>
<type>asset</type>
<filename></filename>
<text></text>
<sha256></sha256>
</link>
""".strip()
    text_asset_link_element = datajack.Element.from_string(text_asset_link_tree)
    embedded_asset_link_tree = """
<link>
<type>asset</type>
<filename></filename>
<embed_asset>
  <type>image</type>
  <caption></caption>
</embed_asset>
<sha256></sha256>
</link>
""".strip()
    embedded_asset_link_element = datajack.Element.from_string(embedded_asset_link_tree)
    # Check formatting of all asset links.
    # Also build lists of each type of asset link.
    text_asset_links = []
    embedded_asset_links = []
    for asset_link in asset_links:
      result2, msg2 = asset_link.matches_tree_of(text_asset_link_element)
      # Use contains_tree_of, because embed_asset_link may also have a 'text' element.
      result3, msg3 = asset_link.contains_tree_of(embedded_asset_link_element)
      if not result2 and not result3:
        msg = msg2 if result2 else msg3
        raise ValueError(msg)
      if result2:
        text_asset_links.append(asset_link)
      if result3:
        embedded_asset_links.append(asset_link)
    unique_asset_names = list(set([x.get_value('filename') for x in asset_links]))
    msg = "Assets: {} asset links found in article, containing {} unique filenames.".format(len(asset_links), len(unique_asset_names))
    if len(embedded_asset_links) > 0:
      msg += " {} are embedded asset links.".format(len(embedded_asset_links))
    log(msg)
    # Check if asset directory exists.
    article_dir = os.path.dirname(article_file)
    default = 'assets'
    default_asset_dir = join(article_dir, default)
    asset_dir_exists = False
    if isdir(asset_dir) or isdir(default_asset_dir):
      asset_dir_exists = True
    if isdir(asset_dir) and isdir(default_asset_dir):
      msg = 'In article_dir ({}), found both the article asset directory ({}) and the default asset directory ({}). Exactly one is permitted.'.format(repr(article_dir), repr(basename(asset_dir)), repr(basename(default_asset_dir)))
      raise ValueError(msg)
    if not isdir(asset_dir) and not isdir(default_asset_dir):
      # Only raise an error if we actually have asset links in the article.
      if len(asset_links) > 0:
        msg = 'In article_dir ({}), did not find either the article asset directory ({}) or the default asset directory ({}). Exactly one is required.'.format(repr(article_dir), repr(basename(asset_dir)), repr(basename(default_asset_dir)))
        raise ValueError(msg)
    if isdir(default_asset_dir):
      asset_dir = default_asset_dir
    # Analyse assets and compare them to asset links.
    if not asset_dir_exists:
      msg = "Assets: No asset directory found."
      log(msg)
    else:
      # Check if this article has any deleted_assets.
      deleted_asset_names = []  # Default.
      if not deleted_assets_element:
        log("No deleted_assets_element supplied.")
        # If a default deleted_assets file is present in settings, load it.
        deleted_assets_settings_file = '../../settings/deleted_assets.txt'
        try:
          das = pkgutil.get_data(__name__, deleted_assets_settings_file)
          das = das.decode('ascii').strip()
          deleted_assets_element = datajack.Element.from_string(das)
          msg = "Default deleted_assets file loaded from: {}".format(deleted_assets_settings_file)
          log(msg)
        except FileNotFoundError:
          msg = "No default deleted_assets file found at: {}".format(deleted_assets_settings_file)
          log(msg)
      if deleted_assets_element and hasattr(a, 'daid'):
        entries = deleted_assets_element.get('article[@id={}]'.format(a.daid))
        if len(entries) > 0:
          # This article has at least one asset that has been deleted.
          deleted_asset_names = entries[0].get_one('asset_names').text
          deleted_asset_names = deleted_asset_names.strip().split('\n')
      # Look at assets in asset_dir.
      asset_names = os.listdir(asset_dir)
      asset_files = [join(asset_dir, x) for x in asset_names]
      msg = "Assets: {} asset files found in asset directory ({}).".format(len(asset_files), repr(asset_dir))
      log(msg)
      # Raise an error if we find assets but have no asset links in the article.
      if len(asset_links) == 0:
        msg = "Found {} assets in asset directory ({})".format(len(asset_names), repr(asset_dir))
        msg += ", but found 0 asset links in article."
        raise ValueError(msg)
      # Check that asset filenames match asset link filenames.
      # Note: There may be multiple asset links for a single actual asset.
      asset_names2 = [x.get_value('filename') for x in asset_links]
      info_msg = "\n- Asset directory: {}".format(asset_dir)
      info_msg += "\n- Number of assets: {}".format(len(asset_names))
      info_msg += "\n- Number of asset links within article: {}".format(len(asset_names2))
      info_msg += "\n- Assets in asset directory:"
      info_msg += '\n-- ' + '\n-- '.join(asset_names)
      info_msg += "\n- Unique filenames in asset links:"
      info_msg += '\n-- ' + '\n-- '.join(list(set(asset_names2)))
      for asset_name in asset_names:
        if asset_name not in asset_names2:
          msg = "Asset not found in list of asset links within article."
          msg += "\n- Asset filename: {}".format(repr(asset_name))
          msg += info_msg
          raise ValueError(msg)
      msg = "Assets: All assets are linked at least once from the article."
      log(msg)
      for asset_name2 in asset_names2:
        if asset_name2 not in asset_names:
          if asset_name2 in deleted_asset_names:
            msg = "Assets: Asset file {} not found in asset dir, but (according to the information in the deleted assets file) this asset has been deleted.".format(repr(asset_name2))
            log(msg)
          else:
            msg = "Asset filename in asset link not found in list of assets in asset directory."
            msg += "\n- Filename in asset link: {}".format(repr(asset_name2))
            msg += info_msg
            raise ValueError(msg)
      msg = "Assets: All asset links map to an asset in the asset directory."
      log(msg)
      # Calculate asset hash values and confirm that they match the hash values in the asset links.
      for asset_file in asset_files:
        asset_name = basename(asset_file)
        asset_bytes = open(asset_file, "rb").read()
        # We'll always use the shell SHA256.
        cmd = 'shasum -a 256 {}'.format(asset_file)
        output, exit_code = util.misc.run_local_cmd(cmd)
        sha256_calc = output.split(' ')[0]
        # We'll use Python SHA256 only if the asset is (approx) less than 1 MB. It's slow.
        if len(asset_bytes) < 10**6:
          sha256_calc_2 = util.misc.pypy_sha256(asset_bytes)
          sha256_calc_3 = util.sha256.SHA256(asset_bytes).hexdigest()
          hashes = [sha256_calc, sha256_calc_2, sha256_calc_3]
          if len(set(hashes)) != 1:
            msg = "Calculated SHA256 hash of asset ({}) in 3 different ways, which don't all agree.".format(asset_name)
            msg += "\nFrom shell: shasum -a 256 <filepath>:"
            msg += "\n" + sha256_calc
            msg += "\nFrom Python2 SHA256 (in util directory):"
            msg += "\n" + sha256_calc_2
            msg += "\nFrom Python3 SHA256 (in util directory):"
            msg += "\n" + sha256_calc_3
            logger.error(msg)  # For now, just log this.
            #raise ValueError(msg)
          else:
            msg = "Calculated SHA256 hash of asset ({}) in 3 different ways, which agree.".format(asset_name)
            msg += "\nFrom shell: shasum -a 256 <filepath>:"
            msg += "\n" + sha256_calc
            msg += "\nFrom Python2 SHA256 (in util directory):"
            msg += "\n" + sha256_calc_2
            msg += "\nFrom Python3 SHA256 (in util directory):"
            msg += "\n" + sha256_calc_3
            deb(msg)
        # Get list of links to this specific asset.
        asset_links3 = [x for x in asset_links if x.get_value('filename') == asset_name]
        for asset_link in asset_links3:
          sha256_link = asset_link.get_value('sha256')
          if sha256_link != sha256_calc:
            msg = "Asset link sha256 value does not match calculated sha256 value."
            msg += "\n- Asset filename: {}".format(asset_name)
            msg += "\n- Asset link:"
            msg += "\n" + asset_link.data
            msg += "\n- Asset link sha256 value:"
            msg += "\n" + sha256_link
            msg += "\n- Calculated sha256 value of asset file:"
            msg += "\n" + sha256_calc
            #print(msg + "\n")
            raise ValueError(msg)
      msg = "Assets: For each asset, the sha256 value has been re-calculated. All links to this asset contain the expected sha256 value."
      log(msg)
  return a




def stop(msg=None):
  if msg is not None:
    print(msg)
  import sys
  sys.exit()
