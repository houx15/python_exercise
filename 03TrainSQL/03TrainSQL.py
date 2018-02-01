"""
Train tickets query via command line

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help    显示帮助菜单
    -g           高铁
    -d           动车
    -t           特快
    -k           快速
    -z           直达

Example:
    tickets beijing shanghai 2018-01-31
"""

from docopt import docopt
from get_station import stations
from prettytable import PrettyTable
import requests

def cli():
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']

    url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'
    url = url.format(date, from_station, to_station)

    r = requests.get(url, verify=False)
    print(r)

class TrainCollection(object):

    header = 'train station time duration first second softsleep hardsleep hardsit'.split()

