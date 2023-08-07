
from SplashDrone import SplashDrone
import time

drone = SplashDrone()
drone.connect(log_dir=None, log_tag=None)
drone.mission_stop(wait_for_ack=False)
for i in range(3):
  drone.task_execute(*drone.get_cmd_land(), wait_for_ack=False)
  time.sleep(0.5)
drone.disconnect()


