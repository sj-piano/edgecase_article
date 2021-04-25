# Imports
import string




# Relative imports
from . import validate as v




def uri_title(t):
  # Example:
  # Stalky_&_Co._by_Rudyard_Kipling:_"In_Ambush"
  # becomes
  # stalky__co__by_rudyard_kipling_in_ambush
  # Example:
  # Recipe_for_installing_Kafka_2.5.0_as_a_systemd_service_on_Ubuntu_16.04
  # becomes
  # recipe_for_installing_kafka_2_5_0_as_a_systemd_service_on_ubuntu_16_04
  v.validate_string(t)
  t = t.lower()
  # Remove punctuation, except for periods and hyphens.
  t2 = ''
  permitted = string.ascii_lowercase + string.digits + '_' + '.-'
  for c in t:
    if c in permitted:
      # Replace periods and hyphens with underscores.
      # Goal: URI titles should be selectable as a whole via a double-click.
      # We use them as "spacing" so that we can do versioning properly.
      # E.g. 'foo_25' in a title is distinguished from 'foo_2.5'.
      if c in '.-': c = '_'
      t2 += c
  return t2