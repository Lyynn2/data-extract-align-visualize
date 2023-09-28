
############
#
# Copyright (c) 2023 Joseph DelPreto / MIT CSAIL and Project CETI
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
# IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Created 2023 by Joseph DelPreto [https://josephdelpreto.com].
# [can add additional updates and authors as desired]
#
############

from collections import OrderedDict
from helpers_data_extraction import *

############################################
# CONFIGURATION
############################################

# The path to the root of the data directory,
#   which contains subfolders for each requested device.
data_root_dir = 'path_to_data_root_folder'
assert data_root_dir != 'path_to_data_root_folder', 'Please remember to update the variable "data_root_dir"'

# The device IDs from which to extract data.
annotation_sources = [
  '_coda_annotations_biology',
  '_coda_annotations_haifa',
]

############################################
# EXTRACT DATA
############################################

# For each annotation source (biology or haifa), will create a dictionary combining data from all coda annotation files.
#   The dictionary keys are as follows:
#     coda_start_times_s: each entry is a coda start time
#     coda_end_times_s  : each entry is a coda end time
#     click_icis_s      : each entry is a list of ICIs for that coda
#     click_times_s     : each entry is a list of click times for clicks in that coda
#     whale_indexes     : each entry is a whale index; indexes over 20 indicate uncertain annotations (see Shane's readme for more information)
#  All lists in the dictionary are the same length, with each entry describing the coda at that index.
# Timestamps are aligned using a manually determined offset for the underlying audio device.

# Will also create lists of start/end times of the audio files that were annotated.

print()
print('Getting all coda annotations')
(codas_data, codas_audio_files_start_times_s, codas_audio_files_end_times_s) = \
    get_timestamped_data_codas(data_root_dir,
                               device_ids=annotation_sources, device_friendlyNames=None,
                               suppress_printing=False)
   
############################################
# SAMPLE USAGE
############################################

print()
print('='*50)
print()

for annotation_source in codas_data:
  print('See device id: %s' % annotation_source)
  # Get the data for this annotation source.
  coda_data = codas_data[annotation_source]
  coda_audio_files_start_times_s = codas_audio_files_start_times_s[annotation_source]
  coda_audio_files_end_times_s = codas_audio_files_end_times_s[annotation_source]
  coda_start_times_s = coda_data['coda_start_times_s']
  coda_end_times_s = coda_data['coda_end_times_s']
  click_icis_s = coda_data['click_icis_s']
  click_times_s = coda_data['click_times_s']
  whale_indexes = coda_data['whale_indexes']
  # Unwrap lists of lists to get one list of all clicks instead of a list per coda.
  click_times_s_all = [click_time_s for coda_click_times_s in click_times_s for click_time_s in coda_click_times_s]
  click_icis_s_all = [click_ici_s for coda_icis_s in click_icis_s for click_ici_s in coda_icis_s]
  # Print a summary.
  num_codas = len(coda_start_times_s)
  num_clicks = sum([len(click_times_s_forCoda) for click_times_s_forCoda in click_times_s])
  print('  Annotations spanned %d audio files (%d seconds)' %
        (len(coda_audio_files_start_times_s),
        sum([coda_audio_files_end_times_s[i] - coda_audio_files_start_times_s[i] for i in range(len(coda_audio_files_start_times_s))])))
  print('  Total number of codas         : %d' % (num_codas))
  print('  Total number of clicks        : %d' % (num_clicks))
  print('  Average clicks per coda       : %0.2f' % (num_clicks/num_codas))
  print('  Average coda duration         : %0.2f seconds' % (np.mean([coda_end_times_s[i] - coda_start_times_s[i] for i in range(num_codas)])))
  print('  Average | Min | Max ICI       : %d | %d | %d milliseconds' % (1000*np.mean(click_icis_s_all), 1000*np.min(click_icis_s_all), 1000*np.max(click_icis_s_all)))
  print('  Unique whale indexes          : %d' % (len(set(whale_indexes))))
  print('  Unique "certain" whale indexes: %d' % (len(set([whale_index for whale_index in whale_indexes if whale_index < 20]))))
  print('  Uncertain codas               : %d' % (len([whale_index for whale_index in whale_indexes if whale_index >= 20])))
  
