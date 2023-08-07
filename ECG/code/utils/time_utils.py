
import time
from datetime import datetime
from dateutil import tz


# Get a date string from seconds since epoch.
# If time_s is None, will use the current time.
def get_time_str(time_s=None, format='%Y-%m-%d_%H-%M-%S', return_time_s=False):
  time_s = time_s or time.time()
  time_datetime = datetime.fromtimestamp(time_s)
  time_str = time_datetime.strftime(format)
  if return_time_s:
    return (time_str, time_s)
  else:
    return time_str

# Given a UTC time string in the format %H:%M:%S.%f,
#  add the current UTC date then convert it to local time and return seconds since epoch.
def get_time_s_from_utc_timeNoDate_str(time_utc_str, input_time_format='%H:%M:%S.%f',
                                       date_utc_str=None, input_date_format='%Y-%m-%d'):
  from_zone = tz.tzutc()
  to_zone = tz.tzlocal()
  
  # Get the current UTC date if no date was provided.
  if date_utc_str is None:
    now_utc_datetime = datetime.utcnow()
    date_utc_str = now_utc_datetime.strftime(input_date_format)
  
  # Combine the date and time.
  utc_str = '%s %s' % (date_utc_str, time_utc_str)
  utc_datetime = datetime.strptime(utc_str, input_date_format + ' ' + input_time_format)
  
  # Convert to local time, then to seconds since epoch.
  utc_datetime = utc_datetime.replace(tzinfo=from_zone)
  local_datetime = utc_datetime.astimezone(to_zone)
  return local_datetime.timestamp()







