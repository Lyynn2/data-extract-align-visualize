
import os
import time
import dateutil.parser
from PIL import Image

dir = 'P:/Media/Pictures/2023/2023-07 Dominica/_BOAT_2023-07-08/David'
#dir = 'path_to_david_photos_folder'
fp = os.path.join(dir, 'IMG_4790.1688812736000.jpg') # his first photo
#fp = os.path.join(dir, 'IMG_6558.1688831949000.jpg') # his last photo

# Define the timezone offset of the metadata.
# If this is set to -0000, then the resulting epoch time matches the one in the original filname.
# If this is set to -0400, then the result epoch time seems correct (and matches the drones).
timezone_offset_str = '-0400' 

# Get the date taken
# This yields a reasonable local time in ET.
img = Image.open(fp)
date_taken_local_str = img._getexif()[36867]
(year, month, day, hour, minute, second) = date_taken_local_str.replace(' ', ':').split(':')

# Add the timezone information to the string.
date_taken_local_str = '%s-%s-%s %s:%s:%s %s' % (year, month, day, hour, minute, second, timezone_offset_str)

# Convert
date_taken_datetime = dateutil.parser.parse(date_taken_local_str)
date_taken_epoch_s = date_taken_datetime.timestamp()

# Print
print('date taken str:', date_taken_local_str)
print('date taken epoch [s]', date_taken_epoch_s)

