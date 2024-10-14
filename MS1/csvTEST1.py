import csv
import time
from seeed_dht import DHT

sensor = DHT('11', 18)
# pin = 18
while True:
    hu, temp = sensor.read()
    print('temp:{0:0.1f} hu:{1}'.format(temp, hu))
    time.sleep(1)
    data = [hu, temp]

with open('hu_temp.csv', 'w') as file:
	writer = csv.writer(file)
    writer.writerow(data)
