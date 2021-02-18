# xiaomiair
Xiaomi Mi Air Purifier automation using python-miio lib in docker

User value:
Having non-CN versions of Xiaomi Mi Air Purifier devices, automation capabilities differ from those that CN based.

This project aims to create python code that can be turned into docker image and run automation according to following specs.

1. Code automates single device - requires separate containers to automate multiple devices.
2. Refresh air function - turns on fan with user specified freqency for specified time, on specified fan level. For night this is optional with separate fan level setting.
2. Scheduler works following way:
  - allows to define 6 Aqi levels, every with separate fan level.
  - for night to not disturb users - every level has this limit set
  - day hours and night hours can be defined
  - polling Aqi with user specified interval:
    - when last 3 reads of AQI are above trigger_on (example 10),  set fan mode on selected level when day
                                                                   set fan mode on max level for night
    - when last 3 reads of AQI are below trigger_off (example 10), set fan mode on selected level (0) when day
                                                                   set fan mode on selected level (0) when night

User settings are applied via environment variables:
  DEVICE_IP=<IPv4 only>
  TOKEN=<token>
  MODEL=<2 or 3>
  SCHEDULER_INTERVAL=<value in seconds>
  AQI_LEVEL_DISABLE=<must be lower than any other AQI_LEVEL_X>
  AQI_LEVEL_1=<int from 10 to 160>
  FAN_LEVEL_1=<int from 1 to 12>
  AQI_LEVEL_2=<int from 10 to 160>
  FAN_LEVEL_2=<int from 1 to 12>
  AQI_LEVEL_3=<int from 10 to 160>
  FAN_LEVEL_3=<int from 1 to 12>
  AQI_LEVEL_4=<int from 10 to 160>
  FAN_LEVEL_4=<int from 1 to 12>
  AQI_LEVEL_5=<int from 10 to 160>
  FAN_LEVEL_5=<int from 1 to 12>
  AQI_LEVEL_6=<int from 10 to 160>
  FAN_LEVEL_6=<int from 1 to 12>
  FAN_LEVEL_NIGHT=<int from 1 to 12>
  REFRESH_AIR_INTERVAL=<value in seconds>
  REFRESH_AIR_DURATION=<value in seconds>
  REFRESH_AIR_FAN_LEVEL_DAY=<int from 1 to 12>
  REFRESH_AIR_FAN_LEVEL_NIGHT=<int from 1 to 12>
  REFRESH_AIR_ON_NIGHT=<True or False>
  BEGIN_DAY_HOUR=<int from 0 to 23>
  BEGIN_NIGHT_HOUR=<int from 0 to 23>
