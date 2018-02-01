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
from stations import stations
from prettytable import PrettyTable
import requests
import json

def cli():
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']

    url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'
    url = url.format(date, from_station, to_station)

    r = requests.get(url, verify=False)
    #text = bytes.decode(r.content)
    #print(r.json())
    maps = r.json()['data']['map']
    rows = r.json()['data']['result']

    trains = TrainCollection(rows, maps)
    trains.pretty_print()
    

class TrainCollection(object):

    header = 'train station time duration vip first second vip-ssleep softsleep dsleep hardsleep softsit hardsit nosit'.split()

    def __init__(self, rows, maps):
        formatted_rows = []
        for row in rows:
            row_format = {}
            row_data = row.split('|')
            row_format['station_train_code'] = row_data[2]
            row_format['from_station_name'] = maps[row_data[3]]
            row_format['to_station_name'] = maps[row_data[4]]
            row_format['start_time'] = row_data[7]
            row_format['arrive'] = row_data[8]
            row_format['lishi'] = row_data[9]
            row_format['vip'] = row_data[-5]
            row_format['zy_num'] = row_data[-6]
            row_format['ze_num'] = row_data[-7]
            row_format['rw_num'] = row_data[-8]
            row_format['dw_num'] = row_data[-9]
            row_format['yw_num'] = row_data[-10]
            row_format['rz_num'] = row_data[-11]
            row_format['yz_num'] = row_data[-12]
            row_format['wz_num'] = row_data[-13]
        self.rows = rows

    def _get_duration(self, row):
        duration = row.get('lishi').replace(':', 'h') + 'm'
        if duration.startswith('00'):
            return duration[4:]
        if duration.startswith('0'):
            return duration[1:]
        return duration

    @property
    def trains(self):
        for row in self.rows:
            train = [
                row['station_train_code'],
                '\n'.join([row['from_station_name'], row['to_station_name']]),
                '\n'.join([row['start_time'], row['arrive']]),
                self._get_duration(row),
                row['vip'],
                row['zy_num'],
                row['ze_num'],
                row['rw_num'],
                row['dw_num'],
                row['yw_num'],
                row['rz_num'],
                row['yz_num'],
                row['wz_num']
            ]
            yield train

    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        
        print(pt)


if __name__ == '__main__':
    cli()