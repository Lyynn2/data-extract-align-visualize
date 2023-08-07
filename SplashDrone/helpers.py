
from KBHit import KBHit
import time

# Helper to convert hex values to integers.
# If the input is an array of bytes, will return an array of integers.
# It the input is not bytes (e.g. already an integer), will return the input unchanged.
def hex_to_int(to_convert):
  if isinstance(to_convert, bytes):
    if len(to_convert) > 1:
      return [hex_to_int(x) for x in to_convert]
    else:
      return int.from_bytes(to_convert, byteorder='little', signed=False)
  else:
    return to_convert

# Helper to convert integer values to bytes (hex).
# If the input is an array of integers, will return a byte array.
# It the input is not integers (e.g. already bytes), will return the input unchanged.
def int_to_hex(to_convert):
  if not isinstance(to_convert, bytes):
    if isinstance(to_convert, (list, tuple)):
      res = b''
      for x in to_convert:
        res += int_to_hex(x)
      return res
    else:
      return int.to_bytes(to_convert, length=1, byteorder='little', signed=False)
  else:
    return to_convert

# Helper to get a printable string from a hex byte array.
def get_hex_str(to_print):
  return '[%s]' % ' '.join(['0x%s' % format(x, '02x') for x in to_print])


# Wait for the specified duration or until the user presses enter/space.
def wait_s(duration_s):
  print()
  print()
  print('Waiting for %0.2f seconds... press enter or space to abort' % duration_s)
  print()
  kb = KBHit()
  user_input = None
  start_time_s = time.time()
  while time.time() - start_time_s < duration_s and user_input is None:
    if kb.kbhit():
      c = kb.getch()
      if ord(c) in [ord(x) for x in ['\r', '\n', ' ']]:
        return c
  return True









