
from SplashDrone import SplashDrone
import os
script_dir = os.path.dirname(os.path.realpath(__file__))
import time

from helpers import *
from utils.print_utils import *
from utils.time_utils import *

data_dir = os.path.realpath(os.path.join(script_dir, 'data'))
log_dir = os.path.join(data_dir, '%s testing outside' % get_time_str(format='%Y-%m-%d'))
log_tag = 'takeOff_land'

# If the user aborts any waiting period, will skip all subsequent stages and land/disconnect.
user_intervened = False

# Connect to the drone!
drone = SplashDrone()
drone.connect(log_dir=log_dir, log_tag=log_tag)
user_intervened = not wait_s(10)

########################################
# Build and run a mission.
########################################
print('RUNNING A MISSION')
mission_typesAndDatas = []
# mission_typesAndDatas.append(drone.get_cmd_setSpeed(speed_cm_s=30))
# mission_typesAndDatas.append(drone.get_cmd_setAltitude_relativeToTakeoffAltitude(
#                                                    relative_altitude_cm=10))
mission_typesAndDatas.append(drone.get_cmd_setSpeed(speed_cm_s=100))
mission_typesAndDatas.append(drone.get_cmd_takeOff(target_altitude_cm=75))
# mission_typesAndDatas.append(drone.get_cmd_setAltitude_relativeToTakeoffAltitude(
#                                                    relative_altitude_cm=10))
# mission_typesAndDatas.append(drone.get_cmd_addWaypoint(latitude=423613563, longitude=-710902913, hover_time_s=5))
# mission_typesAndDatas.append(drone.get_cmd_addWaypoint(latitude=423613563, longitude=-710903070, hover_time_s=5))
# mission_typesAndDatas.append(drone.get_cmd_addWaypoint(latitude=423613563, longitude=-710902913, hover_time_s=5))
# mission_typesAndDatas.append(drone.get_cmd_land())
drone.mission(mission_typesAndDatas=mission_typesAndDatas, execute_immediately=True)

user_intervened = not wait_s(10)

lat_home = int(drone._flight_statuses['latitude'][-1])
lon_home = int(drone._flight_statuses['longitude'][-1])
lat_target = lat_home + 500
lon_target = lon_home - 500

mission_typesAndDatas = []
# mission_typesAndDatas.append(drone.get_cmd_setSpeed(speed_cm_s=30))
# mission_typesAndDatas.append(drone.get_cmd_setSpeed(speed_cm_s=100))
# mission_typesAndDatas.append(drone.get_cmd_setAltitude_relativeToTakeoffAltitude(
#                                                    relative_altitude_cm=50))
# mission_typesAndDatas.append(drone.get_cmd_takeOff(target_altitude_cm=75))
# mission_typesAndDatas.append(drone.get_cmd_setAltitude_relativeToTakeoffAltitude(
#                                                    relative_altitude_cm=10))
# mission_typesAndDatas.append(drone.get_cmd_addWaypoint(latitude=423613563, longitude=-710902913, hover_time_s=5))
mission_typesAndDatas.append(drone.get_cmd_addWaypoint(latitude=lat_target, longitude=lon_target, hover_time_s=20))
mission_typesAndDatas.append(drone.get_cmd_addWaypoint(latitude=lat_home, longitude=lon_home, hover_time_s=20))
# mission_typesAndDatas.append(drone.get_cmd_land())
drone.mission(mission_typesAndDatas=mission_typesAndDatas, execute_immediately=True)

user_intervened = not wait_s(60)





# mission_typesAndDatas = []
# # mission_typesAndDatas.append(drone.get_cmd_setSpeed(speed_cm_s=30))
# # mission_typesAndDatas.append(drone.get_cmd_setAltitude_relativeToTakeoffAltitude(
# #                                                    relative_altitude_cm=10))
# # mission_typesAndDatas.append(drone.get_cmd_takeOff(target_altitude_cm=75))
# # mission_typesAndDatas.append(drone.get_cmd_addWaypoint(latitude=423613563, longitude=-710902913, hover_time_s=5))
# mission_typesAndDatas.append(drone.get_cmd_addWaypoint(latitude=423613563, longitude=-710903070, hover_time_s=5))
# # mission_typesAndDatas.append(drone.get_cmd_addWaypoint(latitude=423613563, longitude=-710902913, hover_time_s=5))
# # mission_typesAndDatas.append(drone.get_cmd_land())
# drone.mission(mission_typesAndDatas=mission_typesAndDatas, execute_immediately=True)
#
# user_intervened = not wait_s(15)

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






