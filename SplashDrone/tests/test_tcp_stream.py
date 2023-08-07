
import socket
import time

ip = '192.168.2.1'
port = 2022
address = (ip, port)
start_flag = b'\xa6'
msg_ids = {
  'flight_status': b'\x1d',
}

def read_bytes(message, start_index, num_bytes, convert_to_int=False):
  if None in [message, start_index, num_bytes]:
    res = None
    next_index = None
  elif start_index + num_bytes <= len(message):
    res = message[start_index : (start_index + num_bytes)]
    next_index = start_index + num_bytes
  else:
    res = None
    next_index = None
  if convert_to_int and res is not None:
    res = hex_to_int(res)
  return res, next_index

def hex_to_int(to_convert):
  return int.from_bytes(to_convert, byteorder='little', signed=False)

def get_hex_str(to_print):
  return '[%s]' % ' '.join(['0x%s' % format(x, '02x') for x in to_print])
  
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
  sock.connect(address)
  data = b''
  start_time_s = time.time()
  while True:
    data += sock.recv(512)
    # print('%7.3f' % (time.time() - start_time_s), get_hex_str(data))
    start_index = data.find(start_flag)
    if start_index < 0:
      data = b''
    while start_index >= 0:
      # print('%7.3f: Parsing received data of length %d with start code at index %d' %
      #       (time.time() - start_time_s, len(data), start_index))
      # print(get_hex_str(data[start_index:]))
      index = start_index
      _, index = read_bytes(data, index, 1, convert_to_int=False) # start flag
      packet_length, index = read_bytes(data, index, 1, convert_to_int=True)
      if packet_length is None:
        # print('No packet length')
        break # not enough data in the buffer yet
      if len(data) - start_index < packet_length:
        # print('Not enough length (packet length %d)' % packet_length)
        break # not enough data in the buffer yet
      msg_id, index = read_bytes(data, index, 1, convert_to_int=False)
      src, index = read_bytes(data, index, 1, convert_to_int=False)
      dest, index = read_bytes(data, index, 1, convert_to_int=False)
      payload, index = read_bytes(data, index, packet_length-6, convert_to_int=False)
      checksum, index = read_bytes(data, index, 1, convert_to_int=False)
      print('time %7.3f | start index %2d | start flag %s | packet length %g | src %s | dest %s | msg_id %s | checksum %g payload-sum %g' %
            (time.time() - start_time_s, start_index,
             get_hex_str(start_flag), packet_length,
             get_hex_str(src), get_hex_str(dest), get_hex_str(msg_id),
             hex_to_int(checksum), sum(payload)))
      # Process the message.
      if msg_id == msg_ids['flight_status']:
        pass
      # Look for another message in the data
      data = data[index:]
      start_index = data.find(start_flag)
      # print('second start index?', start_index)
