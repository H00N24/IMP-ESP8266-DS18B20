AMPY = ampy --port /dev/ttyUSB0
FILES = boot.py esp_temp.py conf.json

default: ls

ls:
	$(AMPY) ls

all: boot temp conf

boot: 
	$(AMPY) put boot.py

temp:
	$(AMPY) put esp_temp.py

conf:
	$(AMPY) put conf.json

term:
	picocom /dev/ttyUSB0 -b115200

clear:
	for f in $(FILES); do $(AMPY) rm $$f ; done