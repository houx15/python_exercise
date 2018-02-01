import re
import requests
from pprint import pprint

url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=4.0'
r = requests.get(url, verify=False)
text = bytes.decode(r.content)
#print(text)
stations = re.findall('([A-Z]+)\|([a-z]+)', text)
#print(stations)
stations = dict(stations)
stations = dict(zip(stations.values(), stations.keys()))
#print(stations)
pprint(stations, indent = 4)