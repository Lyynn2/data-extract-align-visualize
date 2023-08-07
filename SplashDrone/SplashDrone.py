
import socket
import threading
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
script_dir = os.path.dirname(os.path.realpath(__file__))
import time

from helpers import *
from utils.print_utils import *
from utils.time_utils import *

#############################################
# A class to interface with the SplashDrone 4
#############################################
class SplashDrone:
  
  #########################
  ###### Definitions ######
  #########################
  msg_start_flag = b'\xa6'
  msg_ids = {
    'flight_status'             : b'\x1d',
    'waypoint_mission_status'   : b'\x31',
    'flight_mission_control'    : b'\x34',
    'gimbal_position_broadcast' : b'\x30',
  }
  msg_device_ids = {
    'flight_control'    : b'\x01',
    'remote_controller' : b'\x02',
    'gimbal'            : b'\x03',
    'app'               : b'\x04',
    'report'            : b'\xff',
    'self'              : b'\x00',
    'custom_min'        : b'\xc8',
    'custom_max'        : b'\xfe',
  }
  msg_opcodes = {
    'FC_TASK_OC_TRAN_STR' : b'\x01',  # Start sending
    'FC_TASK_OC_ADD'      : b'\x03',  # Add mission to queue
    'FC_TASK_OC_READ'     : b'\x04',  # Read mission on queue
    'FC_TASK_OC_START'    : b'\x05',  # Execute mission from the assigned location
    'FC_TASK_OC_STOP'     : b'\x06',  # Stop the current mission immediately
    'FC_TASK_OC_ERROR'    : b'\xfb',  # Error Message
    'FC_TASK_OC_ACK'      : b'\xfc',  # Acknowledge
    'FC_TASK_OC_ACTION'   : b'\xfd',  # Execute the received mission immediately
    'FC_TASK_OC_CLEAR'    : b'\xfe',  # Clear mission queue
    'FC_TASK_OC_TRAN_END' : b'\xff',  # Sending ends
  }
  msg_task_types = {
    'FC_TSK_Null'     : int_to_hex(0),
    'FC_TSK_TakeOff'  : int_to_hex(1),  # Take Off
    'FC_TSK_Land'     : int_to_hex(2),  # Land
    'FC_TSK_RTH'      : int_to_hex(3),  # Return to Home
    'FC_TSK_SetHome'  : int_to_hex(4),  # Set Home Point
    'FC_TSK_SetPOI'   : int_to_hex(5),  # Set Point-of-Interest
    'FC_TSK_DelPOI'   : int_to_hex(6),  # Delete Point-of Interest
    'FC_TSK_Move'     : int_to_hex(7),  # Control Movement in 3D
    'FC_TSK_Gimbal'   : int_to_hex(8),  # Control Gimbal Angle
    'FC_TSK_SetEXTIO' : int_to_hex(9),  # Control External IO (Payload Release, arm lights, strobe light)
    'FC_TSK_WayPoint' : int_to_hex(10),  # Add Waypoint
    'FC_TSK_SetSpeed' : int_to_hex(11),  # Set Flight Speed
    'FC_TSK_SetAlt'   : int_to_hex(12),  # Set Flight Altitude
    'FC_TSK_WAIT_MS'  : int_to_hex(15),  # Set Hover Time
    'FC_TSK_REPLAY'   : int_to_hex(16),  # Set Times of Repetition
    'FC_TSK_CAMERA'   : int_to_hex(17),  # Control Camera
    'FC_TSK_RESERVE'  : int_to_hex(18),  # Reserve
    'FC_TSK_CIRCLE'   : int_to_hex(19),  # Orbit Flight
  }
  checksum_CRC8_table = np.array([
    0, 94, 188, 226, 97, 63, 221, 131, 194, 156, 126, 32, 163, 253, 31, 65,
    157, 195, 33, 127, 252, 162, 64, 30, 95, 1, 227, 189, 62, 96, 130, 220,
    35, 125, 159, 193, 66, 28, 254, 160, 225, 191, 93, 3, 128, 222, 60, 98,
    190, 224, 2, 92, 223, 129, 99, 61, 124, 34, 192, 158, 29, 67, 161, 255,
    70, 24, 250, 164, 39, 121, 155, 197, 132, 218, 56, 102, 229, 187, 89, 7,
    219, 133, 103, 57, 186, 228, 6, 88, 25, 71, 165, 251, 120, 38, 196, 154,
    101, 59, 217, 135, 4, 90, 184, 230, 167, 249, 27, 69, 198, 152, 122, 36,
    248, 166, 68, 26, 153, 199, 37, 123, 58, 100, 134, 216, 91, 5, 231, 185,
    140, 210, 48, 110, 237, 179, 81, 15, 78, 16, 242, 172, 47, 113, 147, 205,
    17, 79, 173, 243, 112, 46, 204, 146, 211, 141, 111, 49, 178, 236, 14, 80,
    175, 241, 19, 77, 206, 144, 114, 44, 109, 51, 209, 143, 12, 82, 176, 238,
    50, 108, 142, 208, 83, 13, 239, 177, 240, 174, 76, 18, 145, 207, 45, 115,
    202, 148, 118, 40, 171, 245, 23, 73, 8, 86, 180, 234, 105, 55, 213, 139,
    87, 9, 235, 181, 54, 104, 138, 212, 149, 203, 41, 119, 244, 170, 72, 22,
    233, 183, 85, 11, 136, 214, 52, 106, 43, 117, 151, 201, 74, 20, 246, 168,
    116, 42, 200, 150, 21, 75, 169, 247, 182, 232, 10, 84, 215, 137, 107, 53
  ], dtype=np.uint8)

  ########################
  ###### INITIALIZE ######
  ########################
  def __init__(self):
    # Define the drone connection information.
    self._drone_socket_ip = '192.168.2.1'
    self._drone_socket_port = 2022
    self._drone_socket_address = (self._drone_socket_ip, self._drone_socket_port)
    self._drone_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self._program_device_id = self.msg_device_ids['custom_min']
    # Set up logging.
    self._log = []
    self._log_headings = [
      'Time [s]', 'Time', 'Time since start [s]',
      'Message ID', 'Message Source ID', 'Message Destination ID',
      'Message Length', 'Parsed Data', 'Raw Message'
    ]
    self._log_fout = None
    self._log_filename = None
    self._flight_statuses = None
    self._waypoint_statuses = None
    self._flight_commands = None
    self._acks = None
    
    # Will increment the mission/task ID after every command.
    self._mission_id = None
    self._mission_id_min = 1   # note that 0 is used to indicate starting a mission from the first task
    self._mission_id_max = 254 # note that 255 is used for clearing the queue
    
    # Initialize state.
    self._listening = False
    self._start_time_s = None
  
  # A helper to get a mission ID to use, after advancing it to avoid repeats.
  def _get_next_mission_id(self):
    if self._mission_id is None:
      self._mission_id = int_to_hex(self._mission_id_min)
    else:
      self._mission_id = hex_to_int(self._mission_id)
      self._mission_id = ((self._mission_id - self._mission_id_min + 1) % ((self._mission_id_max+1) - self._mission_id_min)) + self._mission_id_min
      self._mission_id = int_to_hex(self._mission_id)
    return self._mission_id

  # Connect to the drone, start listening for messages, and optionally start writing to a log.
  def connect(self, log_dir=None, log_tag=''):
    self._start_time_s = time.time()
    # Connect to the drone.
    print('Connecting to the drone at %s on port %d ... ' % (self._drone_socket_address[0], self._drone_socket_address[1]), end='')
    self._drone_socket.connect(self._drone_socket_address)
    print('success!')
    # Start a log file if desired.
    if log_dir is not None:
      self._log_dir = log_dir
      self._log_filename = ('%s_droneLog_%s' % (get_time_str(format='%Y-%m-%d_%H-%M-%S'), log_tag)).strip('_')
      self._log_filename = '%s.csv' % self._log_filename
      log_filepath = os.path.join(log_dir, 'complete_log', self._log_filename)
      print('Starting a log file at %s' % os.path.realpath(log_filepath))
      os.makedirs(os.path.split(log_filepath)[0], exist_ok=True)
      self._log_fout = open(log_filepath, 'w')
      self._log_fout.write(','.join(self._log_headings))
    # Start listening for drone broadcasts in the background.
    self._listening = True
    self._listen_thread = threading.Thread(target=self._listening_loop)
    self._listen_thread.start()
  
  # Disconnect from the drone and stop logging.
  def disconnect(self):
    # Try to stop and land the drone.
    print()
    print()
    try:
      print('SHUTTING DOWN - TRYING TO STOP THE DRONE MISSION')
      self.mission_stop(wait_for_ack=False)
      time.sleep(0.1)
    except:
      pass
    try:
      print('SHUTTING DOWN - TRYING TO LAND THE DRONE')
      self.task_execute(*self.get_cmd_land(), wait_for_ack=False)
      time.sleep(0.1)
    except:
      pass
    time.sleep(2) # Try to get some updated status messages from the drone
    print()
    # Stop the background thread.
    print('Stopping the listening thread')
    self._listening = False
    time.sleep(0.1)
    # Close the log file.
    if self._log_fout is not None:
      # Close the main log file.
      print('Closing the log file')
      self._log_fout.close()
      self._log_fout = None
      # Write a file dedicated to flight statuses, with separate columns for each field.
      log_status_filepath = os.path.join(self._log_dir, 'flight_status_log', '%s_flight_statuses.csv' % os.path.splitext(self._log_filename)[0])
      os.makedirs(os.path.split(log_status_filepath)[0], exist_ok=True)
      with open(log_status_filepath, 'w') as status_fout:
        status_headings = None
        prev_msg_is_cmd = False
        prev_msg_is_ack = False
        for log_index, (time_s, parsed_message) in enumerate(self._log):
          if parsed_message['msg_id'] == self.msg_ids['flight_status']:
            if status_headings is None:
              status_headings = ['Time [s]', 'Time', 'Time since start [s]']
              status_headings.extend(['is_after_cmd'])
              status_headings.extend(['is_after_ack'])
              num_headings_before_statuses = len(status_headings)
              status_headings.extend(list(parsed_message['parsed_data'].keys()))
              status_fout.write(','.join(status_headings))
            to_write = [time_s, get_time_str(time_s, format='%Y-%m-%d %H:%M:%S.%f'), time_s - self._start_time_s]
            to_write.append(int(prev_msg_is_cmd))
            to_write.append(int(prev_msg_is_ack))
            for key in status_headings[num_headings_before_statuses:]:
              to_write.append(parsed_message['parsed_data'][key])
            status_fout.write('\n')
            status_fout.write(','.join([str(x).replace(',', ' | ') for x in to_write]))
            prev_msg_is_cmd = False
            prev_msg_is_ack = False
          if (parsed_message['msg_id'] == self.msg_ids['flight_mission_control'] and parsed_message['src_id'] == self._program_device_id):
            prev_msg_is_cmd = True
          if (parsed_message['msg_id'] == self.msg_ids['flight_mission_control'] and parsed_message['src_id'] == self.msg_device_ids['flight_control']):
            prev_msg_is_ack = True
      # Write a file dedicated to waypoint statuses, with separate columns for each field.
      log_status_filepath = os.path.join(self._log_dir, 'waypoint_status_log', '%s_waypoint_statuses.csv' % os.path.splitext(self._log_filename)[0])
      os.makedirs(os.path.split(log_status_filepath)[0], exist_ok=True)
      with open(log_status_filepath, 'w') as status_fout:
        status_headings = None
        prev_msg_is_cmd = False
        prev_msg_is_ack = False
        for log_index, (time_s, parsed_message) in enumerate(self._log):
          if parsed_message['msg_id'] == self.msg_ids['waypoint_mission_status'] and parsed_message['parsed_data'] is not None:
            if status_headings is None:
              status_headings = ['Time [s]', 'Time', 'Time since start [s]']
              status_headings.extend(['is_after_cmd'])
              status_headings.extend(['is_after_ack'])
              num_headings_before_statuses = len(status_headings)
              status_headings.extend(list(parsed_message['parsed_data'].keys()))
              status_fout.write(','.join(status_headings))
            to_write = [time_s, get_time_str(time_s, format='%Y-%m-%d %H:%M:%S.%f'), time_s - self._start_time_s]
            to_write.append(int(prev_msg_is_cmd))
            to_write.append(int(prev_msg_is_ack))
            for key in status_headings[num_headings_before_statuses:]:
              to_write.append(parsed_message['parsed_data'][key])
            status_fout.write('\n')
            status_fout.write(','.join([str(x).replace(',', ' | ') for x in to_write]))
            prev_msg_is_cmd = False
            prev_msg_is_ack = False
          if (parsed_message['msg_id'] == self.msg_ids['flight_mission_control'] and parsed_message['src_id'] == self._program_device_id):
            prev_msg_is_cmd = True
          if (parsed_message['msg_id'] == self.msg_ids['flight_mission_control'] and parsed_message['src_id'] == self.msg_device_ids['flight_control']):
            prev_msg_is_ack = True
      # Write a pickle of the log too.
      log_pickle_filepath = os.path.join(self._log_dir, 'pickled_log', '%s.pickle' % os.path.splitext(self._log_filename)[0])
      os.makedirs(os.path.split(log_pickle_filepath)[0], exist_ok=True)
      with open(log_pickle_filepath, 'wb') as pickle_fout:
        pickle.dump(self._log, pickle_fout)
      # Clear the log filepath to help indicate that the log is closed.
      self._log_filepath = None
    # Wait for the background thread to stop.
    self._listen_thread.join()
    # Close the drone socket.
    try:
      print('Closing the drone socket... ', end='')
      self._drone_socket.close()
      print('done')
    except:
      print('WARNING: Error closing the drone socket')
    print()
    
  def visualize_status(self):
    self._statuses_fig, axs = plt.subplots(
        nrows=2, ncols=2,
        squeeze=False, # if False, always return 2D array of axes
        sharex=True, sharey=False,
        subplot_kw={'frame_on': True},
        figsize=(11.5, 6.0)
    )
    try:
      self._statuses_fig.canvas.manager.window.wm_geometry("+%d+%d" % (0, 0))
    except:
      pass
    self._statuses_axs = {
      'altitude'   : axs[0][0],
      'speed'      : axs[1][0],
      'throttle'   : axs[1][0].twinx(),
      'orientation': axs[0][1],
      'state'      : axs[1][1],
    }
    
    # Plot the data.
    plot_start_time_s = time.time()
    # for (key, ax) in self._statuses_axs.items():
    #   for artist in ax.lines + ax.collections:
    #     artist.remove()
    t = [time_s - self._start_time_s for time_s in self._flight_statuses['time_s']]
    self._statuses_axs['altitude'].plot(t, np.array(self._flight_statuses['altitude_m']) * 100, '-*')
    h_st1 = self._statuses_axs['speed'].plot(t, np.array(self._flight_statuses['speed_horizontal_m_s']) * 100, '-*', label='Horizontal')
    h_st2 = self._statuses_axs['speed'].plot(t, np.array(self._flight_statuses['speed_vertical_m_s']) * 100, '-*', label='Vertical')
    h_st3 = self._statuses_axs['throttle'].plot(t, np.array(self._flight_statuses['throttle_percent']), '-*', label='Throttle', color='y')
    self._statuses_axs['state'].plot(t, np.array(self._flight_statuses['is_flying']) * 1.0, '-*', label='Flying')
    self._statuses_axs['state'].plot(t, np.array(self._flight_statuses['is_landing']) * 1.1, '-*', label='Landing')
    self._statuses_axs['state'].plot(t, np.array(self._flight_statuses['is_rising']) * 1.2, '-*', label='Rising')
    self._statuses_axs['state'].plot(t, np.array(self._flight_statuses['is_returning']) * 1.3, '-*', label='Returning')
    self._statuses_axs['orientation'].plot(t, np.array(self._flight_statuses['pitch_deg']), '-*', label='Pitch')
    self._statuses_axs['orientation'].plot(t, np.array(self._flight_statuses['roll_deg']), '-*', label='Roll')
    self._statuses_axs['orientation'].plot(t, np.array(self._flight_statuses['yaw_deg']), '-*', label='Yaw')
    # Show times of commands and acks.
    acks_t = [t - self._start_time_s for t in self._acks['time_s']]
    cmds_t = [t - self._start_time_s for t in self._flight_commands['time_s']]
    for (key, ax) in self._statuses_axs.items():
      for cmd_t in cmds_t:
        ax.axvline(x=cmd_t, linestyle='-', color='r')
      for ack_t in acks_t:
        ax.axvline(x=ack_t, linestyle='--', color='g')
    # Formatting
    for (key, ax) in self._statuses_axs.items():
      if len(cmds_t) > 2:
        ax.set_xlim([max(min(cmds_t)-1, min(ax.get_xlim())),
                     min(max(cmds_t)+6, max(ax.get_xlim()))])
      ax.set_xlabel('Time since start [s]')
      ax.grid(True, color='lightgray')
    self._statuses_axs['altitude'].set_title('Altitude')
    # self._statuses_axs['altitude'].set_ylim([-50, min([200, max(self._statuses_axs['altitude'].get_ylim())])])
    self._statuses_axs['altitude'].set_ylabel('Altitude [cm]')
    self._statuses_axs['throttle'].set_ylabel('Throttle [\%]')
    self._statuses_axs['speed'].set_title('Speed')
    self._statuses_axs['speed'].set_ylabel('Speed [cm/s]')
    h_st = h_st1 + h_st2 + h_st3
    self._statuses_axs['speed'].legend(h_st, [l.get_label() for l in h_st])
    self._statuses_axs['state'].set_title('Flight State')
    self._statuses_axs['state'].legend()
    self._statuses_axs['orientation'].set_title('Orientation')
    self._statuses_axs['orientation'].set_ylabel('Orientation [deg]')
    self._statuses_axs['orientation'].legend()
    # self._statuses_fig.canvas.draw()
    # self._statuses_fig.canvas.flush_events()
    print('Updated the status graphs in %0.2fs' % (time.time() - plot_start_time_s))
    # Save the figure.
    if self._log_dir is not None:
      plt.show(block=False)
      time.sleep(0.5)
      fig_filepath = os.path.join(self._log_dir, 'flight_status_log', '%s_statusesFig' % os.path.splitext(self._log_filename)[0])
      try:
        plt.savefig('%s.png' % fig_filepath, dpi=300)
        plt.savefig('%s.pdf' % fig_filepath)
        with open('%s.pickle' % fig_filepath, 'wb') as fig_fout:
          pickle.dump(self._statuses_fig, fig_fout)
      except:
        print('\n\nCould not save the status figure.\n\n')
    plt.show(block=True)
    
    
  ##########################################
  ###### Drone mission/task interface ######
  ##########################################
  
  # Prepare and send a message.
  def send_message(self, msg_id, src_id, dest_id, payload):
    # Create a message with the following structure:
    #  start_flag | msg_length | msg_id | src_id | dest_id | payload | checksum
    msg_length = len(payload) + 6
    msg = b''
    msg += SplashDrone.msg_start_flag
    msg += int.to_bytes(msg_length, length=1, byteorder='little', signed=False)
    msg += msg_id
    msg += src_id
    msg += dest_id
    msg += payload
    msg += self.compute_checksum(msg, 1, len(msg)-1)
    if msg_id == self.msg_ids['flight_mission_control']:
      parsed_data = {
        'opcode': int_to_hex(payload[0]),
        'mission_id': int_to_hex(payload[1]),
        'mission_type': int_to_hex(payload[2]) if len(payload) >= 3 else None,
        'mission_data': payload[3:] if len(payload) >= 4 else None,
      }
      # Log the command.
      if self._flight_commands is None:
        self._flight_commands = dict([(key, []) for key in parsed_data])
        self._flight_commands['time_s'] = []
      for key in parsed_data:
        self._flight_commands[key].append(parsed_data[key])
      self._flight_commands['time_s'].append(time.time())
    else:
      parsed_data = None
    self._log_msg({
                    'msg_id': msg_id,
                    'src_id': src_id,
                    'dest_id': dest_id,
                    'msg_length': msg_length,
                    'payload': payload,
                    'parsed_data': parsed_data,
                    'raw_msg': msg,
                  }, time.time())
    self._drone_socket.send(msg)
    return msg
  
  # Helper to send a mission-related command.
  def send_mission_command(self, opcode, mission_id,
                           mission_type=None, mission_data=None, wait_for_ack=False, ack_timeout_s=None):
    msg_id = self.msg_ids['flight_mission_control']
    src_id = self._program_device_id
    dest_id = self.msg_device_ids['flight_control']
    payload = b''
    payload += opcode
    payload += mission_id
    if mission_type is not None:
      payload += mission_type
    if mission_data is not None:
      payload += mission_data
    # Send the message!
    self.send_message(msg_id=msg_id, src_id=src_id, dest_id=dest_id, payload=payload)
    # Wait for acknowledgment if desired.
    if wait_for_ack:
      def received_ack():
        if len(self._log) == 0:
          return False
        last_msg = self._log[-1][1]
        correct_id = last_msg['msg_id'] == self.msg_ids['flight_mission_control']
        try:
          correct_opcode = last_msg['parsed_data']['opcode'] == self.msg_opcodes['FC_TASK_OC_ACK']
          # If it is a command with a valid mission ID, check the returned type and ID.
          # Otherwise, assume it is a command such as STOP that uses a pre-coded ID and that has weird return values in the ack.
          if hex_to_int(mission_id) >= self._mission_id_min and hex_to_int(mission_id) <= self._mission_id_max:
            correct_mission_type = last_msg['parsed_data']['mission_type'] == mission_type
            correct_mission_id = last_msg['parsed_data']['mission_id'] == mission_id
          else:
            correct_mission_type = True
            correct_mission_id = True
        except:
          correct_opcode = False
          correct_mission_id = False
          correct_mission_type = False
        return (correct_id and correct_opcode and correct_mission_id and correct_mission_type)
      ack_timeout_s = 2 if ack_timeout_s is None else ack_timeout_s
      start_time_s = time.time()
      while (not received_ack()) and ((time.time() - start_time_s) < ack_timeout_s):
        pass
      if (time.time() - start_time_s) >= ack_timeout_s:
        print('WARNING: did not receive task acknowledgment for message ID %s opcode %s type %s' %
              (get_hex_str(msg_id), get_hex_str(opcode), get_hex_str(mission_type) if mission_type is not None else 'None'))
        return False
    return True
    
  # Clear the queue of tasks in the mission.
  def mission_clear_queue(self, wait_for_ack=False):
    return self.send_mission_command(opcode=self.msg_opcodes['FC_TASK_OC_CLEAR'],
                                     mission_id=b'\x00', mission_type=None, mission_data=None,
                                     wait_for_ack=wait_for_ack)
  
  # Start adding tasks to the mission.
  def mission_start_transmission(self, wait_for_ack=False):
    self._get_next_mission_id() # Advance the mission ID
    return self.send_mission_command(opcode=self.msg_opcodes['FC_TASK_OC_TRAN_STR'],
                                     mission_id=b'\xFF', mission_type=None, mission_data=None,
                                     wait_for_ack=wait_for_ack)
  # Stop adding tasks to the mission.
  def mission_end_transmission(self, wait_for_ack=False):
    return self.send_mission_command(opcode=self.msg_opcodes['FC_TASK_OC_TRAN_END'],
                                     mission_id=b'\xFF', mission_type=None, mission_data=None,
                                     wait_for_ack=wait_for_ack)
    
  # Add a task to the mission.
  def mission_add(self, mission_type, mission_data, wait_for_ack=False):
    return self.send_mission_command(opcode=self.msg_opcodes['FC_TASK_OC_ADD'],
                                     mission_id=self._mission_id,
                                     mission_type=mission_type, mission_data=mission_data,
                                     wait_for_ack=wait_for_ack)
  
  # Execute the mission, either from the beginning or from the previous task if it was stopped.
  def mission_execute(self, start_from='beginning', wait_for_ack=False):
    if start_from.lower().strip() == 'beginning':
      mission_id = b'\x00'
    elif start_from.lower().strip() == 'previous':
      mission_id = b'\xFF'
    else:
      raise AssertionError('Unknown mission starting task identifier')
    return self.send_mission_command(opcode=self.msg_opcodes['FC_TASK_OC_START'],
                                     mission_id=mission_id, mission_type=None, mission_data=None,
                                     wait_for_ack=wait_for_ack)
  
  # Stop the current execution and make the aircraft hover.
  def mission_stop(self, wait_for_ack=False):
    return self.send_mission_command(opcode=self.msg_opcodes['FC_TASK_OC_STOP'],
                                     mission_id=b'\x00', mission_type=None, mission_data=None,
                                     wait_for_ack=wait_for_ack)
  
  # Helper to build a mission and execute it.
  def mission(self, mission_types=None, mission_datas=None, mission_typesAndDatas=None, execute_immediately=False):
    print('MISSION')
    if mission_typesAndDatas is not None:
      mission_types = [info[0] for info in mission_typesAndDatas]
      mission_datas = [info[1] for info in mission_typesAndDatas]
    # Stop/clear any existing mission.
    print('Stopping existing mission')
    if not self.mission_stop(wait_for_ack=True): return False
    print('Clearing mission queue')
    if not self.mission_clear_queue(wait_for_ack=True): return False
    # Start a new mission transmission.
    print('Starting mission transmission')
    if not self.mission_start_transmission(wait_for_ack=True): return False
    # Populate the mission with the desired tasks.
    for i in range(len(mission_types)):
      print('Adding a task to the mission')
      if not self.mission_add(mission_type=mission_types[i], mission_data=mission_datas[i],
                              wait_for_ack=True):
        return False
    # End the mission transmission.
    print('Ending the transmission')
    if not self.mission_end_transmission(wait_for_ack=True): return False
    # Execute the mission if desired.
    if execute_immediately:
      print('Executing the mission')
      if not self.mission_execute(start_from='beginning', wait_for_ack=True): return False
    return True
  
  # Helper to run a single task now.
  def task_execute(self, mission_type, mission_data, wait_for_ack=False, ack_timeout_s=None):
    self._get_next_mission_id() # Advance the mission ID
    return self.send_mission_command(opcode=self.msg_opcodes['FC_TASK_OC_ACTION'],
                                     mission_id=self._mission_id,
                                     mission_type=mission_type, mission_data=mission_data,
                                     wait_for_ack=wait_for_ack, ack_timeout_s=ack_timeout_s)
  
  ############################
  ###### Drone control! ######
  ############################
  
  # target_altitude_cm can be from 0-65535 cm
  def get_cmd_takeOff(self, target_altitude_cm):
    task_type = self.msg_task_types['FC_TSK_TakeOff']
    task_data = int.to_bytes(target_altitude_cm, length=2, byteorder='little', signed=False)
    return (task_type, task_data)
    
  def get_cmd_land(self):
    task_type = self.msg_task_types['FC_TSK_Land']
    task_data = None
    return (task_type, task_data)
    
  def get_cmd_returnHome(self):
    task_type = self.msg_task_types['FC_TSK_RTH']
    task_data = None
    return (task_type, task_data)
  
  # Latitude and longitude are ±1800000000
  def get_cmd_setHome(self, latitude, longitude):
    task_type = self.msg_task_types['FC_TSK_SetHome']
    task_data = b''
    task_data += int.to_bytes(latitude,  length=4, byteorder='little', signed=True)
    task_data += int.to_bytes(longitude, length=4, byteorder='little', signed=True)
    return (task_type, task_data)
  
  # Relative distances can be ±32767cm, but will be rounded down to 10 cm increments.
  # Horizontal speed can be 0 - 2500 cm/s
  # Vertical   speed can be ±400 cm/s
  def get_cmd_move(self, forward_cm, left_cm, up_cm, speed_horizontal_cm_s, speed_vertical_cm_s):
    task_type = self.msg_task_types['FC_TSK_Move']
    task_data = b''
    task_data += int.to_bytes(forward_cm, length=2, byteorder='little', signed=True)
    task_data += int.to_bytes(left_cm, length=2, byteorder='little', signed=True)
    task_data += int.to_bytes(up_cm, length=2, byteorder='little', signed=True)
    task_data += int.to_bytes(int(speed_horizontal_cm_s/10), length=1, byteorder='little', signed=False)
    task_data += int.to_bytes(int(speed_vertical_cm_s/10), length=1, byteorder='little', signed=True)
    return (task_type, task_data)
  
  # Speed can be 0 - 65535 cm/s
  def get_cmd_setSpeed(self, speed_cm_s):
    speed_m_s = speed_cm_s/100
    task_type = self.msg_task_types['FC_TSK_SetSpeed']
    task_data = b''
    task_data += int.to_bytes(int(speed_m_s*100), length=2, byteorder='little', signed=False)
    return (task_type, task_data)
  
  # Relative altitude can be 0 - 65535 cm
  def get_cmd_setAltitude_relativeToTakeoffAltitude(self, relative_altitude_cm):
    relative_altitude_m = relative_altitude_cm/100
    task_type = self.msg_task_types['FC_TSK_SetAlt']
    task_data = b''
    task_data += int.to_bytes(int(relative_altitude_m*100), length=2, byteorder='little', signed=False)
    return (task_type, task_data)

  # Latitude and longitude are ±1800000000
  # Hover time can be 0 - 65535 s
  def get_cmd_addWaypoint(self, latitude, longitude, hover_time_s):
    task_type = self.msg_task_types['FC_TSK_WayPoint']
    task_data = b''
    task_data += int.to_bytes(int(hover_time_s), length=2, byteorder='little', signed=False)
    task_data += int.to_bytes(int(latitude), length=4, byteorder='little', signed=True)
    task_data += int.to_bytes(int(longitude), length=4, byteorder='little', signed=True)
    return (task_type, task_data)
    

  ##############################
  ###### Receive messages ######
  ##############################

  def _listening_loop(self):
    buffer = b''
    while self._listening:
      # Receive data from the socket.
      buffer += self._drone_socket.recv(128)
      # See if the start flag is present in the buffer.
      start_index = buffer.find(self.msg_start_flag)
      # print(start_index, self.msg_start_flag, get_hex_str(buffer))
      # Clear the buffer if no start flag is present.
      if start_index < 0:
        buffer = b''
      # Try to parse the message.
      (postMessage_index, parsed_message) = self._parse_message(buffer)
      if parsed_message is not None:
        # Clear the parsed message from the buffer.
        buffer = buffer[postMessage_index:]
        # Log the message.
        self._log_msg(parsed_message)
  
  # Parse a message with the following structure:
  #  start_flag | msg_length | msg_id | src_id | dest_id | payload | checksum
  # Returns (start_index, parsed_message) where start_index is the index into the buffer
  #  after the parsed message ends.
  # Returns (None, None) if a valid message was not parsed.
  def _parse_message(self, buffer):
    # Initial validation to make sure that at least meta information is present.
    start_index = buffer.find(self.msg_start_flag)
    if start_index < 0:
      return (None, None)
    if (len(buffer) - start_index) < 6:
      return (None, None)
    
    # Get the message length and check if the whole message is received yet.
    start_flag = int_to_hex(buffer[start_index])
    msg_length = int(buffer[start_index + 1])
    if (len(buffer) - start_index) < msg_length:
      return (None, None)
    end_index = (start_index + msg_length - 1)
    msg = buffer[start_index:(end_index+1)]
    # Unpack the rest of the message.
    msg_id = int_to_hex(msg[2])
    src_id = int_to_hex(msg[3])
    dest_id = int_to_hex(msg[4])
    payload = msg[5:-1]
    checksum = int_to_hex(msg[-1])
    # print(start_flag, msg_length, get_hex_str(msg_id), get_hex_str(src_id), get_hex_str(dest_id), len(payload), get_hex_str(payload), get_hex_str(checksum))
    
    # Confirm that the start flag was read correctly.
    if start_flag != self.msg_start_flag:
      print('WARNING: Invalid message start flag in message', get_hex_str(msg))
      return (None, None)
    # Verify the checksum.
    if not self.verify_checksum(msg):
      print('WARNING: Checksum does not match.')
      return (None, None)
      
    # Parse status messages.
    parsed_data = None
    if msg_id == self.msg_ids['flight_status']:
      parsed_data = self._parse_flight_status(payload)
    elif msg_id == self.msg_ids['flight_mission_control']:
      parsed_data = self._parse_task_acknowledgment(payload)
    elif msg_id == self.msg_ids['waypoint_mission_status']:
      parsed_data = self._parse_waypoint_status(payload)
    
    # Return the parsed information.
    next_start_index = end_index+1
    return (next_start_index, {
                                'msg_id': msg_id,
                                'src_id': src_id,
                                'dest_id': dest_id,
                                'msg_length': msg_length,
                                'payload': payload,
                                'parsed_data': parsed_data,
                                'raw_msg': msg,
                              })
  
  # Parse a flight status payload.
  def _parse_flight_status(self, payload):
    if len(payload) != 44:
      print('WARNING: Invalid flight status payload length. Expected %d got %d' % (44, len(payload)))
    # Helper to read bytes, convert to an integer, and advance the index.
    def read_bytes(buffer, index, length, convert_to_int, signed, scale=1.0):
      res = buffer[index:(index+length)]
      if convert_to_int:
        res = int.from_bytes(res, byteorder='little', signed=signed)
        res = res*scale
      return index+length, res
    
    # Extract and parse bytes from the struct.
    index = 0
    # Pitch, roll, and yaw: int16_t, unit 0.1deg
    index, pitch_deg = read_bytes(payload, index, 2, convert_to_int=True, signed=True, scale=0.1)
    index, roll_deg = read_bytes(payload, index, 2, convert_to_int=True, signed=True, scale=0.1)
    index, yaw_deg = read_bytes(payload, index, 2, convert_to_int=True, signed=True, scale=0.1)
    # Horizontal fly speed: uint16, unit 0.1m/s
    index, speed_horizontal_m_s = read_bytes(payload, index, 2, convert_to_int=True, signed=False, scale=0.1)
    # Altitude: int16, unit 0.1m
    index, altitude_m = read_bytes(payload, index, 2, convert_to_int=True, signed=True, scale=0.1)
    # Home Distance: uint16, unit 1m
    index, home_distance_m = read_bytes(payload, index, 2, convert_to_int=True, signed=False, scale=1)
    # Voltage: int16, unit 0.1V
    index, voltage_v = read_bytes(payload, index, 2, convert_to_int=True, signed=True, scale=0.1)
    # GPS heading: int16, unit 0.1deg
    index, gps_heading_deg = read_bytes(payload, index, 2, convert_to_int=True, signed=True, scale=0.1)
    # Home heading: int16, unit 0.1deg +-1800
    index, home_heading_deg = read_bytes(payload, index, 2, convert_to_int=True, signed=True, scale=0.1)
    # Fly time: uint16, unit 1sec
    index, fly_time_s = read_bytes(payload, index, 2, convert_to_int=True, signed=False, scale=1)
    # Longitude/Latitude of drone: int32
    # NOTE: Based on tests, the documentation is correct to say lon, lat for the drone but lat, lon for home.
    index, longitude = read_bytes(payload, index, 4, convert_to_int=True, signed=True, scale=1)
    index, latitude  = read_bytes(payload, index, 4, convert_to_int=True, signed=True, scale=1)
    # Longitude/Latitude of takeoff point: int32
    # NOTE: Based on tests, the documentation is correct to say lon, lat for the drone but lat, lon for home.
    index, takeoff_latitude  = read_bytes(payload, index, 4, convert_to_int=True, signed=True, scale=1)
    index, takeoff_longitude = read_bytes(payload, index, 4, convert_to_int=True, signed=True, scale=1)
    # Frame type: uint8, 0:quad   1:boat   2:fixed plane
    index, frame_type  = read_bytes(payload, index, 1, convert_to_int=True, signed=False, scale=1)
    frame_type = {0:'quad', 1:'boat', 2:'fixed_plane'}[frame_type]
    # Motor throttle: uint8, 0-100%
    index, throttle_percent  = read_bytes(payload, index, 1, convert_to_int=True, signed=False, scale=1)
    # Vertical speed: int8, unit 0.1m/s
    index, speed_vertical_m_s  = read_bytes(payload, index, 1, convert_to_int=True, signed=True, scale=0.1)
    # Marked as "Don't care": uint8
    index, _  = read_bytes(payload, index, 1, convert_to_int=True, signed=False, scale=1)
    # GPS number of drone: uint8
    index, gps_num  = read_bytes(payload, index, 1, convert_to_int=True, signed=False, scale=1)
    # Named "reserve1" without comment: uint8
    index, _  = read_bytes(payload, index, 1, convert_to_int=True, signed=False, scale=1)
    # Union with individual bit meanings: uint16
    index, data  = read_bytes(payload, index, 2, convert_to_int=True, signed=False, scale=1)
    fly_mode                = (data >>  0) & 0b1111
    is_low_voltage          = (data >>  4) & 0b11
    is_motor_unlocked       = (data >>  6) & 0b1
    rc_signal_lost          = (data >>  7) & 0b1
    ahrs_initializing       = (data >>  8) & 0b1
    altitude_control_failed = (data >>  9) & 0b1
    is_landing              = (data >> 10) & 0b1
    is_rising               = (data >> 11) & 0b1
    is_returning            = (data >> 12) & 0b1
    is_flying               = (data >> 13) & 0b1
    prompt_no_gps           = (data >> 14) & 0b1
    is_high_mobility        = (data >> 15) & 0b1
    try:
      fly_mode = {0:'Manual', 1:'Balance', 2:'ATTI', 3:'GPS', 4:'Cruise', 5:'Headless', 6:'Orbit', 7:'Return-to-Home'}[fly_mode]
    except KeyError:
      fly_mode = 'UNKNOWN(%d)' % fly_mode
    
    # Compile the parsed status.
    parsed_status = {
      # Flight configuration
      'frame_type': frame_type,
      'is_high_mobility': is_high_mobility,
      'is_motor_unlocked': is_motor_unlocked,
      'fly_mode': fly_mode,
      # Flying
      'is_flying': is_flying,
      'is_landing': is_landing,
      'is_rising': is_rising,
      'is_returning': is_returning,
      'fly_time_s': fly_time_s,
      'speed_horizontal_m_s': speed_horizontal_m_s,
      'speed_vertical_m_s': speed_vertical_m_s,
      'throttle_percent': throttle_percent,
      # Orientation
      'pitch_deg': pitch_deg,
      'roll_deg': roll_deg,
      'yaw_deg': yaw_deg,
      'ahrs_initializing': ahrs_initializing,
      # Position
      'altitude_m': altitude_m,
      'latitude': latitude,
      'longitude': longitude,
      'gps_heading_deg': gps_heading_deg,
      'gps_num': gps_num,
      # Home position
      'home_distance_m': home_distance_m,
      'home_heading_deg': home_heading_deg,
      'takeoff_latitude': takeoff_latitude,
      'takeoff_longitude': takeoff_longitude,
      # Voltage
      'voltage_v': voltage_v,
      'is_low_voltage': is_low_voltage,
      # Errors
      'rc_signal_lost': rc_signal_lost,
      'prompt_no_gps': prompt_no_gps,
      'altitude_control_failed': altitude_control_failed,
    }
    
    # Log the parsed status.
    if self._flight_statuses is None:
      self._flight_statuses = dict([(key, []) for key in parsed_status])
      self._flight_statuses['time_s'] = []
    for key in parsed_status:
      self._flight_statuses[key].append(parsed_status[key])
    self._flight_statuses['time_s'].append(time.time())
    # Return the parsed status.
    return parsed_status
  
  def _parse_waypoint_status(self, payload):
    if len(payload) != 19:
      # print('WARNING: Invalid waypoint status payload length. Expected %d got %d' % (19, len(payload)))
      return None
    # Helper to read bytes, convert to an integer, and advance the index.
    def read_bytes(buffer, index, length, convert_to_int, signed, scale=1.0):
      res = buffer[index:(index+length)]
      if convert_to_int:
        res = int.from_bytes(res, byteorder='little', signed=signed)
        res = res*scale
      return index+length, res
    
    nav_states = [
      'NS_NULL',
      'NS_ReadyToFly',
      'NS_Delay',
      'NS_Flying',
      'NS_ReadyToEnd',
      'NS_Complete',
      'NS_Pause',
      ]
    
    # Extract and parse bytes from the struct.
    index = 0
    # A fixed value at the beginning.
    index, fixed_value = read_bytes(payload, index, 1, convert_to_int=True, signed=False)
    if int(fixed_value) != 2:
      print('WARNING: Invalid waypoint status fixed byte. Expected %d got %g' % (2, fixed_value))
    # Nav state
    index, nav_state_index = read_bytes(payload, index, 1, convert_to_int=True, signed=False)
    nav_state_index = int(nav_state_index)
    nav_state = nav_states[nav_state_index]
    # Waypoint number
    index, waypoint_number = read_bytes(payload, index, 1, convert_to_int=True, signed=False)
    index, delay_time_s = read_bytes(payload, index, 1, convert_to_int=True, signed=False)
    index, max_waypoint_number = read_bytes(payload, index, 1, convert_to_int=True, signed=False)
    index, angular_speed_deg_s = read_bytes(payload, index, 1, convert_to_int=True, signed=False)
    index, max_fly_speed_m_s = read_bytes(payload, index, 1, convert_to_int=True, signed=False)
    index, distance_to_waypoint_m = read_bytes(payload, index, 2, convert_to_int=True, signed=False)
    index, path_deviation = read_bytes(payload, index, 2, convert_to_int=True, signed=True)
    index, next_latitude = read_bytes(payload, index, 4, convert_to_int=True, signed=True)
    index, next_longitude = read_bytes(payload, index, 4, convert_to_int=True, signed=True)
    
    # Compile the parsed status.
    parsed_status = {
      # Current state
      'nav_state': nav_state,
      'waypoint_number': waypoint_number,
      'anguler_speed_deg_s': angular_speed_deg_s,
      'path_deviation': path_deviation,
      # Moving on
      'delay_time_s' : delay_time_s,
      'next_latitude' : next_latitude,
      'next_longitude' : next_longitude,
      'distance_to_waypoint_m' : distance_to_waypoint_m,
      # Limits
      'max_waypoint_number' : max_waypoint_number,
      'max_fly_speed_m_s' : max_fly_speed_m_s,
    }
    
    # Log the parsed status.
    if self._waypoint_statuses is None:
      self._waypoint_statuses = dict([(key, []) for key in parsed_status])
      self._waypoint_statuses['time_s'] = []
    for key in parsed_status:
      self._waypoint_statuses[key].append(parsed_status[key])
    self._waypoint_statuses['time_s'].append(time.time())
    # Return the parsed status.
    return parsed_status

  # Parse a task acknowledgment payload.
  def _parse_task_acknowledgment(self, payload):
    if len(payload) < 3:
      print('WARNING: Invalid task acknowledgment payload length. Expected >= %d, got %d' % (3, len(payload)))
    
    opcode = int_to_hex(payload[0])
    mission_id = int_to_hex(payload[1])
    mission_type = int_to_hex(payload[2])
    mission_data = payload[3:]
    parsed_ack = {
      'opcode': opcode,
      'mission_id': mission_id,
      'mission_type': mission_type,
      'mission_data': mission_data,
    }

    # Log the parsed acknowledgment.
    if self._acks is None:
      self._acks = dict([(key, []) for key in parsed_ack])
      self._acks['time_s'] = []
    for key in parsed_ack:
      self._acks[key].append(parsed_ack[key])
    self._acks['time_s'].append(time.time())
    # Return the parsed acknowledgment.
    return parsed_ack
  
  ######################
  ###### Checksums ######
  ######################
  def compute_checksum(self, buffer, offset, length):
    buffer = np.array(hex_to_int(buffer), dtype=np.uint8)
    crc = np.array([0], dtype=np.uint8)
    for j in range(length):
      crc[0] = SplashDrone.checksum_CRC8_table[np.bitwise_xor(crc[0], buffer[offset])]
      offset = offset+1
    return crc[0]
  
  def verify_checksum(self, msg):
    checksum_msg = msg[-1]
    checksum_computed = self.compute_checksum(msg, 1, len(msg)-2) # omit the start flag (first byte) and the checksum (last byte)
    return (checksum_msg == checksum_computed)

  ##############################
  ###### Printing/Logging ######
  ##############################

  def _log_msg(self, parsed_message, time_s=None):
    time_s = time_s or time.time()
    # Record the message.
    self._log.append((time_s, parsed_message))
    # Print the message.
    if(parsed_message['msg_id'] not in [self.msg_ids['waypoint_mission_status'], self.msg_ids['flight_status']]):
    # if(parsed_message['msg_id'] not in [None]):
      print('time %7.3f | msg_id %s | src %s | dest %s | packet length %g | parsed data %s' %
            (time_s - self._start_time_s, get_hex_str(parsed_message['msg_id']),
             get_hex_str(parsed_message['src_id']), get_hex_str(parsed_message['dest_id']),
             parsed_message['msg_length'], parsed_message['parsed_data']))
    # Write the message to a file.
    if self._log_fout is not None:
      parsed_data_strs = parsed_message['parsed_data']
      if isinstance(parsed_data_strs, dict):
        for k in parsed_data_strs:
          if isinstance(parsed_data_strs[k], bytes):
            parsed_data_strs[k] = get_hex_str(parsed_data_strs[k])
      to_write = [time_s, get_time_str(time_s, format='%Y-%m-%d %H:%M:%S.%f'), time_s - self._start_time_s,
                  get_hex_str(parsed_message['msg_id']),
                  get_hex_str(parsed_message['src_id']), get_hex_str(parsed_message['dest_id']),
                  parsed_message['msg_length'], str(parsed_message['parsed_data']),
                  get_hex_str(parsed_message['raw_msg'])
                  ]
      self._log_fout.write('\n')
      self._log_fout.write(','.join([str(x).replace(',', ' | ') for x in to_write]))



#####################
###### TESTING ######
#####################
if __name__ == '__main__':
  # drone = SplashDrone()
  # test_msg = [b'\xa6', b'\x32', b'\x1d', b'\x01', b'\xff', b'\x0b', b'\x00', b'\x02', b'\x00', b'\x3c', b'\xf9', b'\x00', b'\x00', b'\x2a', b'\x00', b'\x00', b'\x00', b'\xa2', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\xfa', b'\x00', b'\x00', b'\x08', b'\x00', b'\x38']
  # test_msg = [hex_to_int(x) for x in test_msg]
  # test_msg = int_to_hex(test_msg)
  # print('msg length:', len(test_msg), hex_to_int(test_msg[1]))
  # # test_msg = [hex_to_int(x) for x in test_msg]
  # print('computed checksum:', drone.compute_checksum(test_msg, 1, len(test_msg)-2))
  # print('checksum verifies?', drone.verify_checksum(test_msg))
  # print(drone._parse_message(test_msg))
  # print_var(drone._parse_message(test_msg)[1]['parsed_data'])

  data_dir = os.path.realpath(os.path.join(script_dir, 'data'))
  log_dir = os.path.join(data_dir, '2022-05-03 testing in holodeck')
  log_tag = 'props_pyControl_mission_lift100-L100-land_speed100'
  
  # If the user aborts any waiting period, will skip all subsequent stages and land/disconnect.
  user_intervened = False
  
  # Connect to the drone!
  drone = SplashDrone()
  drone.connect(log_dir=log_dir, log_tag=log_tag)
  user_intervened = not wait_s(10)

  ########################################
  # Build and run a mission.
  ########################################
  mission_typesAndDatas = []
  mission_typesAndDatas.append(drone.get_cmd_takeOff(target_altitude_cm=100))
  mission_typesAndDatas.append(drone.get_cmd_move(forward_cm=0, left_cm=250, up_cm=0,
                                                  speed_horizontal_cm_s=500,
                                                  speed_vertical_cm_s=500))
  mission_typesAndDatas.append(drone.get_cmd_land())
  drone.mission(mission_typesAndDatas=mission_typesAndDatas, execute_immediately=True)
  user_intervened = not wait_s(15)
  
  # mission_typesAndDatas = []
  # mission_typesAndDatas.append(drone.get_cmd_move(forward_cm=0, left_cm=100, up_cm=0,
  #                                                 speed_horizontal_cm_s=100,
  #                                                 speed_vertical_cm_s=100))
  # drone.mission(mission_typesAndDatas=mission_typesAndDatas, execute_immediately=True)
  # user_intervened = not wait_s(5)
  ########################################
  # Land.
  ########################################
  print('********************** LANDING')
  for i in range(5):
    if drone.task_execute(*drone.get_cmd_land(), wait_for_ack=True, ack_timeout_s=0.5):
      break
  user_intervened = not wait_s(3)
  
  # ########################################
  # # Take off!
  # ########################################
  # if not user_intervened:
  #   print('********************** TAKING OFF')
  #   drone.task_execute(*drone.get_cmd_takeOff(target_altitude_cm=100), wait_for_ack=True)
  #   user_intervened = not wait_s(6)
  # ########################################
  # # Fly!
  # ########################################
  # if not user_intervened:
  #   drone.task_execute(*drone.get_cmd_move(forward_cm=0, left_cm=250, up_cm=0,
  #                                          speed_horizontal_cm_s=500,
  #                                          speed_vertical_cm_s=500), wait_for_ack=True)
  #   user_intervened = not wait_s(5)
  # ########################################
  # # Land.
  # ########################################
  # print('********************** LANDING')
  # for i in range(5):
  #   if drone.task_execute(*drone.get_cmd_land(), wait_for_ack=True, ack_timeout_s=0.5):
  #     break
  # user_intervened = not wait_s(3)
  
  # Disconnect from the drone.
  drone.disconnect()
  drone.visualize_status()






