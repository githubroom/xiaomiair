# xiaomiair
Xiaomi Mi Air Purifier automation using python-miio lib in docker

Having non-CN versions of Xiaomi Mi Air Purifier devices, automation capabilities differ from those that CN based.

This project aims to create python code that can be turned into docker image and run automation according to following specs.

1. Code automates single device - requires multiple containers to automate multiple devices.
2. Scheduler works following way:
  - allows to define day_hours (example 6-19) and night_hours (20-5)
  - poll current AQI (not Average AQI) every minute:
    - when last 3 reads of AQI are above trigger_on (example 10),  set fan mode on selected level for day hours when day
                                                                   set fan mode on selected level for night hours when night
    - when last 3 reads of AQI are below trigger_off (example 10), set fan mode to auto when day
                                                                   set fan mode to night when night

