import os

import yaml

import time

import logging


from datetime import datetime

from xap import xap2, xap3, Aqi


"""
https://python-miio.readthedocs.io/en/latest/api/miio.airpurifier.html
https://python-miio.readthedocs.io/en/latest/api/miio.airpurifier_miot.html
"""
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)

ip = str(os.environ["DEVICE_IP"])

token = str(os.environ["TOKEN"])

scheduler_interval = int(os.environ["SCHEDULER_INTERVAL"])

aqi_level_disable = int(os.environ["AQI_LEVEL_DISABLE"])

aqi_level_1 = int(os.environ["AQI_LEVEL_1"])
fan_level_1 = int(os.environ["FAN_LEVEL_1"])

aqi_level_2 = int(os.environ["AQI_LEVEL_2"])
fan_level_2 = int(os.environ["FAN_LEVEL_2"])

aqi_level_3 = int(os.environ["AQI_LEVEL_3"])
fan_level_3 = int(os.environ["FAN_LEVEL_3"])

aqi_level_4 = int(os.environ["AQI_LEVEL_4"])
fan_level_4 = int(os.environ["FAN_LEVEL_4"])

aqi_level_5 = int(os.environ["AQI_LEVEL_5"])
fan_level_5 = int(os.environ["FAN_LEVEL_5"])

aqi_level_6 = int(os.environ["AQI_LEVEL_6"])
fan_level_6 = int(os.environ["FAN_LEVEL_6"])

fan_level_night = int(
    os.environ["FAN_LEVEL_NIGHT"]
)  # this is max fan level during night_hours

refresh_air_interval = int(os.environ["REFRESH_AIR_INTERVAL"])

refresh_air_duration = int(os.environ["REFRESH_AIR_DURATION"])

refresh_air_fan_level_day = int(os.environ["REFRESH_AIR_FAN_LEVEL_DAY"])

refresh_air_fan_level_night = int(os.environ["REFRESH_AIR_FAN_LEVEL_NIGHT"])

refresh_air_on_night = bool(os.environ["REFRESH_AIR_ON_NIGHT"])

last_refresh_air = None

model = int(os.environ["MODEL"])

begin_day_hour = int(os.environ["BEGIN_DAY_HOUR"])

begin_night_hour = int(os.environ["BEGIN_NIGHT_HOUR"])

day_hours = []
night_hours = []

for hour in range(begin_day_hour, begin_night_hour):
    day_hours.append(hour)
for hour in range(begin_night_hour, 24):
    night_hours.append(hour)
for hour in range(0, begin_day_hour):
    night_hours.append(hour)

hour_now = datetime.now().hour


def main():

    if model == 2:
        purifier = xap2(ip=ip, token=token)
    elif model == 3:
        purifier = xap3(ip=ip, token=token)
    else:
        exit(logging.error(f"Model {model} not recognized."))

    # aqi_level_disable always < aqi_level_x
    if (
        aqi_level_1 < aqi_level_disable
        or aqi_level_2 < aqi_level_disable
        or aqi_level_3 < aqi_level_disable
        or aqi_level_4 < aqi_level_disable
        or aqi_level_5 < aqi_level_disable
        or aqi_level_6 < aqi_level_disable
    ):
        exit(
            logging.error(
                f"AQI_LEVEL_DISABLE must be lower than any other AQI_LEVEL for scheduler to work properly"
            )
        )

    logging.info(f"Initializing scheduler")
    logging.info(f"Day hours:{day_hours}")
    logging.info(f"Night hours: {night_hours}")

    aqi = Aqi(3)
    aqi.initialize()
    # Initialize Aqi to have 3 aqi reads
    for i in range(0, 3):
        aqi.enqueue(int(purifier.get_aqi()))
        time.sleep(10)

    # initialize last_refresh_air time
    last_refresh_air = datetime.now()

    while True:
        seconds_since_last_refresh = int(
            (datetime.now() - last_refresh_air).total_seconds()
        )
        hour_now = datetime.now().hour
        # first check if refresh air is required
        if seconds_since_last_refresh > refresh_air_interval:
            if hour_now in day_hours:
                last_refresh_air = datetime.now()
                logging.info(
                    f"Execute {refresh_air_duration} seconds air refresh in day hours, fan level {refresh_air_fan_level_day}"
                )
                purifier.manual_mode(refresh_air_fan_level_day)
                time.sleep(refresh_air_duration)
            elif (hour_now in night_hours) and refresh_air_on_night:
                last_refresh_air = datetime.now()
                logging.info(
                    f"Execute {refresh_air_duration} seconds air refresh in night hours, fan level {refresh_air_fan_level_night}"
                )
                purifier.manual_mode(refresh_air_fan_level_night)
                time.sleep(refresh_air_duration)

        aqi.enqueue(int(purifier.get_aqi()))

        hour_now = (
            datetime.now().hour
        )  # generate again as when refresh air execute, hour could swich
        logging.info(f"Aqi: {aqi.items}")
        if aqi.is_lower(aqi_level_disable):
            purifier.manual_mode(0)
            logging.info(f"Air is clean now.")
        elif aqi.is_higher(aqi_level_6):
            if hour_now in night_hours:
                purifier.manual_mode(fan_level_night)
                logging.info(
                    f"AQI exceeds {aqi_level_6}, enabling fan level {fan_level_night} for night_hours"
                )
            else:
                purifier.manual_mode(fan_level_6)
                logging.info(
                    f"AQI exceeds {aqi_level_6}, enabling fan level {fan_level_6}"
                )
        elif aqi.is_higher(aqi_level_5):
            if hour_now in night_hours:
                purifier.manual_mode(fan_level_night)
                logging.info(
                    f"AQI exceeds {aqi_level_5}, enabling fan level {fan_level_night} for night_hours"
                )
            else:
                purifier.manual_mode(fan_level_5)
                logging.info(
                    f"AQI exceeds {aqi_level_5}, enabling fan level {fan_level_5}"
                )
        elif aqi.is_higher(aqi_level_4):
            if hour_now in night_hours:
                purifier.manual_mode(fan_level_night)
                logging.info(
                    f"AQI exceeds {aqi_level_4}, enabling fan level {fan_level_night} for night_hours"
                )
            else:
                purifier.manual_mode(fan_level_4)
                logging.info(
                    f"AQI exceeds {aqi_level_4}, enabling fan level {fan_level_4}"
                )
        elif aqi.is_higher(aqi_level_3):
            if hour_now in night_hours:
                purifier.manual_mode(fan_level_night)
                logging.info(
                    f"AQI exceeds {aqi_level_3}, enabling fan level {fan_level_night} for night_hours"
                )
            else:
                purifier.manual_mode(fan_level_3)
                logging.info(
                    f"AQI exceeds {aqi_level_3}, enabling fan level {fan_level_3}"
                )
        elif aqi.is_higher(aqi_level_2):
            if hour_now in night_hours:
                purifier.manual_mode(fan_level_night)
                logging.info(
                    f"AQI exceeds {aqi_level_2}, enabling fan level {fan_level_night} for night_hours"
                )
            else:
                purifier.manual_mode(fan_level_2)
                logging.info(
                    f"AQI exceeds {aqi_level_2}, enabling fan level {fan_level_2}"
                )
        elif aqi.is_higher(aqi_level_1):
            if hour_now in night_hours:
                purifier.manual_mode(fan_level_night)
                logging.info(
                    f"AQI exceeds {aqi_level_1}, enabling fan level {fan_level_night} for night_hours"
                )
            else:
                purifier.manual_mode(fan_level_1)
                logging.info(
                    f"AQI exceeds {aqi_level_1}, enabling fan level {fan_level_1}"
                )
        logging.info(
            f"Waiting {scheduler_interval} seconds for scheduler to execute again."
        )
        time.sleep(scheduler_interval)


if __name__ == "__main__":
    main()

"""
#TODO
19:50-20:00 Refresh room - turn for 10 min max level (sleep 10min in loop after enabling)
15:50-16:00 Refresh room - turn for 10 min max level (sleep 10min in loop after enabling)
every 30min turn on refresh on min level for 1 min
"""
