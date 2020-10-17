from .iparser import IParser
from serializers.iserializer import ISerializer

import requests
from bs4 import BeautifulSoup as bs
import re
from datetime import datetime


days = {
    1: 'mondey',
    2: 'tuesday',
    3: 'wednesday',
    4: 'thursday',
    5: 'friday',
    6: 'saturday',
    0: 'date_col',

}

class TTTParsser(IParser):

    def __init__(self):
        self.data = {}

    def parse(self, url ):
        resp = requests.get(url)

        root_html = bs(resp.text, 'lxml').html
        week_slider = root_html.findAll('div', attrs={'class': 'col-md-12'})
        self.data.update(self._get_current_week(week_slider[1]))
    

        week_timetable = week_slider[3].find('div', {'class': 'table-responsive'})

        
        self.data.update(self._get_timetable(week_timetable))
        
    def clear_cash(self):
        self.data = {}


    def serialize(self, serialaizer: ISerializer) -> str:
        serialaizer.update_properties(self.data)
        return serialaizer.to_str()


    def serialize_dump(self, serialaizer: ISerializer, fout) -> str:
        serialaizer.update_properties(self.data)
        return serialaizer.dumpf(fout)

    @staticmethod
    def create_url_link(group_num:str, fac_name:str, date: int):
        return f'https://timetable.tusur.ru/faculties/{fac_name}/groups/{group_num}?week_id={date}'
    
    @staticmethod
    def get_week_num(date: datetime) -> int:
        ttt_start = datetime(2010, 8, 30, 18, 53, 47, 482342)
        w = (date - ttt_start).days // 7
        return w
    
    def _get_current_week(self, div_weeks) :
        week_info = div_weeks.find('li', {'class' : 'current'}).findAll('div')
        return {'week_info' :{
            'ood': self._remove_spaces_and_ret(week_info[0].text),
            'start_with': self._remove_spaces_and_ret(week_info[1].text)
        }}

        
    def _remove_spaces_and_ret(self, s: str) -> str:
        s = s.replace('\n', '')
        return re.sub(r'\s+', ' ', s).strip()
    
    def _get_timetable(self, tt):
        rez = {}
        thead = tt.find('thead').findAll('th')
        for i, t in enumerate(thead):
            t = t.text
            t = self._remove_spaces_and_ret(t)
            if i != 0:
                rez[i] = ({'date': t, 'day': days[i]})
                rez[i]['subjects_list'] = []
        
        del thead

        tbody = tt.find('tbody')
        for l in range(1, 7):
            cl = f'lesson_{l}'
            row = tbody.find('tr', {'class': cl})
            time = row.find('th', {'class': 'time'}).text
            time = self._remove_spaces_and_ret(time)
            time = f"{time[:5]} - {time[5:]}"
            cols = row.findAll('td')

            

            for i, c in enumerate(cols):
                # c = c.text
                i = i + 1
                net = c.find('div', class_ = 'screen-reader-element')
                d = {
                    'num': l, 
                    'time': time
                }
                if not net:
                    subj= {}
                    subj_info = c.find('div', class_='hidden for_print')
                    subj['full_name'] = subj_info.find('span', class_='discipline').text
                    subj['kind'] = subj_info.find('span', class_='kind').text
                    subj['auditoriums'] = subj_info.find('span', class_='auditoriums').text
                    subj['group'] = subj_info.find('span', class_='group').text
                    note = subj_info.find('span', 'note')
                    if note:
                        subj['note'] = note.text
                    d.update({'subject': subj})
                else:
                    d.update({'subject': net.text})


                rez[i]['subjects_list'].append(d)
            # pprint(d)
        return rez

        


