"""File with ESP_temp class

File contains ESP_tesmp class which is used for
temperature monitoring and communication with server

Author:
    Ondrej Kurak
"""
import network
import ussl as ssl
import socket
import json
from ubinascii import hexlify
from uhashlib import sha1
from machine import Pin
from onewire import OneWire
from ds18x20 import DS18X20


class ESP_temp():
    """Class for temperature monitoring/server communication

    Loading the configuration, connectioning to a wifi,
    temperature monitoring, seding data over SSL socket

    Args:
        conf_file (str): configuration file
        pin (int): DS18B20 pin

    Attributes:
        conf (dict): configuration data
        data (dict): data for server
    """

    def __init__(self, conf_file='conf.json', pin=5):
        self.data = {}
        self.data['TEMP'] = 0

        self.__load_file(conf_file)
        self.__wifi()
        self.__prep_pin(pin)

    def __load_file(self, conf_file):
        """Loading configuration file

        Loads configuration file, server adress,
        wifi SSID and password

        Args:
            conf_file (str): configuration file
        """
        with open(conf_file) as inp:
            self.conf = json.load(inp)

        self.conf['SERVER'] = tuple(self.conf['SERVER'])
        mac = hexlify(network.WLAN().config('mac'), ':')
        pass_hash = sha1(self.conf['OVR'].encode('utf-8'))
        pass_hash = hexlify(pass_hash.digest())

        self.data['MAC'] = mac.decode('utf-8')
        self.data['OVR'] = pass_hash.decode('utf-8')
        self.data['NAME'] = self.conf['NAME']

    def __wifi(self):
        """Connecting to wifi

        Connects to wifi specified in `conf`
        """
        sta_if = network.WLAN(network.STA_IF)
        ap_if = network.WLAN(network.AP_IF)

        ap_if.active(False)
        sta_if.active(True)

        sta_if.connect(self.conf['SSID'], self.conf['PASS'])
        while not sta_if.isconnected():
            pass
        print('Network config:', sta_if.ifconfig())

    def __prep_pin(self, pin):
        """Prepare pin for OneWire device

        Args:
            pin (int): pin with onewire device
        """
        self.ds = DS18X20(OneWire(Pin(pin)))
        self.dev = self.ds.scan()[0]

    def get_temp(self):
        """Reading temperature

        Reading temperature from onewire device

        Returns:
            Temperature
        """
        self.ds.convert_temp()
        self.data['TEMP'] = self.ds.read_temp(self.dev)
        return self.data['TEMP']

    def send_temp(self):
        """Sending actual temperature

        Sends actual temperature over ssl socket
        """
        self.get_temp()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.conf['SERVER'])
        sock = ssl.wrap_socket(sock)
        sock.write(json.dumps(self.data).encode('utf-8'))
