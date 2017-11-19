import re
import logging
import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning


class StacScrapper:

    def __init__(self):
        self.lines = []
        self.stops = []
        self.logger = logging.getLogger(__name__)
        self.BASEURL = 'https://www.bus-stac.fr'
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    @classmethod
    def new(cls):
        return cls()

    def _parse(self, text):
        return BeautifulSoup(text, 'html.parser')

    def get_lines(self, force=False):
        if self.lines and not force:
            return self.lines

        lines = []
        try:
            req = requests.get(self.BASEURL + '/Se-deplacer/Toutes-les-lignes',
                verify=False)
        except:
            return lines

        soup = self._parse(req.text)
        links = soup.find_all('div', class_='links')

        for link in links:
            name = link.find('a').get('href').split('/')[-1]
            directions = link.find('span').string

            r = requests.get('{}/Se-deplacer/Toutes-les-lignes/{}'.format(
                self.BASEURL, name), verify=False)
            s = self._parse(r.text)
            idObj = s.find('input', id='schedules_by_stop_lineId')
            if idObj:
                id = int(idObj.get('value'))
            else:
                id = None
                # do not take into account lines without a valid id
                continue
            
            # remove lines whose number is >= 50
            try:
                numericName = int(name)
                if numericName >= 50:
                    continue
            except ValueError:
                # we keep lines A, B, C, D
                pass
            
            r = re.compile(r'\s*/\s*')
            dirs = r.split(directions)
            self.logger.info('Line {} id is {}'.format(name, id)) 
            lines.append({
                'id': id,
                'name': name,
                'direction1': dirs[0],
                'direction2': dirs[1],
            })
        self.lines = lines
        return lines

    def get_stops(self, force=False):
        if self.stops and not force:
            return self.stops
        stops = []
        lines = self.get_lines()
        for line in lines:
            lineId = line['id']
            lineName = line['name']
            try:
                r = requests.post('{}/Se-deplacer/Toutes-les-lignes/{}'.format(
                    self.BASEURL, lineName),
                    data=(
                        'schedules_by_stop[direction]=1&'
                        'schedules_by_stop[lineId]={}').format(lineId),
                    headers={
                        'X-Requested-With': 
                            'XMLHttpRequest',
                        'Content-Type': 
                            'application/x-www-form-urlencoded; charset=UTF-8'
                    }, 
                    verify=False
                )
            except:
                # TODO: raise issue here
                continue
            s = self._parse(r.text)
            obj = s.find('select', id='schedules_by_stop_stopId')
            order = 0
            for option in obj.find_all('option'):
                logicalId = option.get('data-logicalid')
                if logicalId is None:
                    continue
                id = int(option.get('value'))
                logicalId = int(logicalId)
                stopName = option.string
                order += 1
                self.logger.info('Stop {} id is {}'.format(stopName, id))
                stops.append({
                    'id': id,
                    'order': order,
                    'logical_id': logicalId,
                    'name': stopName,
                    'line_id': lineId,
                })
        self.stops = stops
        return stops


#~ INFO:root:Line 18 id is 4045
#~ {
    #~ 'line_id': '4045',
    #~ 'logical_id': '132946',
    #~ 'name': 'Châtel',
    #~ 'id': '2201071'
#~ }, {
    #~ 'line_id': '4045',
    #~ 'logical_id': '132946',
    #~ 'name': 'Pravaut',
    #~ 'id': '2201072'
#~ }

if __name__ == '__main__':
    s = StacScrapper()
    print(s.get_lines())
    print(s.get_stops())
