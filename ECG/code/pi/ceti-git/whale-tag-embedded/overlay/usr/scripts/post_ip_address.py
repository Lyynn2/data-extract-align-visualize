#!/usr/bin/env python

import time
#time.sleep(60)

import os
import requests
try:
  import netifaces as ni
except ImportError:
  import pip
  os.system("sudo raspi-config nonint do_overlayfs 1")
  pip.main(['install', 'netifaces'])
  os.system("sudo raspi-config nonint do_overlayfs 0")
  import netifaces as ni

def get_ip():
  try:
    ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
    return str(ip)
  except KeyError: # interface was not connected
    return None

url = 'https://docs.google.com/forms/d/e/1FAIpQLSfdSUuPFLx36erla-JRh7HuDWYJiSezd3b-yzwDupwec86jTQ/formResponse'
entry_ids = {'ip':'entry.724467893'}

poll_file_period_s = 30
poll_ip_period_s = 60
kill_filepath = '/home/pi/Desktop/kill_postip_process.txt'

# Wait for connection
print('Waiting for an IP')
while get_ip() is None:
  time.sleep(2)
print('Starting IP: ', get_ip())

# Send the IP whenever it's needed!
next_post_time = time.time()
prev_ip = None
while not os.path.exists(kill_filepath):
  if time.time() >= next_post_time:
    ip = get_ip()
    print('See IP and prev IP:', ip, prev_ip)
    if ip != prev_ip:
      print('Sending IP!')
      print('\n')
      submission = {entry_ids['ip'] : ip}
      requests.post(url, submission)
      prev_ip = ip
    next_post_time = time.time() + poll_ip_period_s
  time.sleep(max(0, min(poll_file_period_s, next_post_time - time.time())))

print('Done!')
print('\n')
if os.path.exists(kill_filepath):
  os.remove(kill_filepath)



