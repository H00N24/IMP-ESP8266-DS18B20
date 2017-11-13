"""Boot file for ESP8266

Starts garbage collector and temperature monitoring.

Note:
    It is nessesary to connect pin 16 to reset pin,
    so deepsleep mode could be activated

Todo:
    * deepsleep after sendig message

Author:
    Ondrej Kurak
"""
import gc
import time
from esp_temp import ESP_temp

gc.collect()

esp = ESP_temp(conf_file='conf.json', pin=5)

esp.send_temp()
