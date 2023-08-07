
from SplashDrone import SplashDrone
import os
script_dir = os.path.dirname(os.path.realpath(__file__))
import time

from helpers import *
from utils.print_utils import *
from utils.time_utils import *

data_dir = os.path.realpath(os.path.join(script_dir, 'data'))
log_dir = os.path.join(data_dir, '%s testing outside' % get_time_str(format='%Y-%m-%d'))
log_tag = 'noOp_readGPS_centerForwardLeftRight'

# If the user aborts any waiting period, will skip all subsequent stages and land/disconnect.
user_intervened = False

# Connect to the drone!
drone = SplashDrone()
drone.connect(log_dir=log_dir, log_tag=log_tag)

########################################
# Stream data while doing nothing.
########################################
user_intervened = not wait_s(300)


########################################
# Make sure it landed
########################################
print('\n'*5)
print('********************** LANDING')
for i in range(5):
  if drone.task_execute(*drone.get_cmd_land(), wait_for_ack=True, ack_timeout_s=0.5):
    break
user_intervened = not wait_s(3)

# Disconnect from the drone.
print('\n'*5)
print('********************** DISCONNECTING')
drone.disconnect()
drone.visualize_status()






