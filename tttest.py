import requests
from bs4 import BeautifulSoup as bs
import sys
import re
import json
from pprint import pprint

from datetime import timedelta, datetime

faculty = {
    0: 'fit',
    1: 'rtf',
    2: 'rkf',
    3: 'fet',
    4: 'fsu',
    5: 'fvs',
    6: 'gf',
    7: 'fb',
    8: 'ef'    
}

days = {
    1: 'mondey',
    2: 'tuesday',
    3: 'wednesday',
    4: 'thursday',
    5: 'friday',
    6: 'saturday',
    0: 'date_col',

}



def get_week_num(date: datetime) -> int:
    ttt_start = datetime(2010, 8, 30, 18, 53, 47, 482342)
    w = (date - ttt_start).days // 7
    return w


def remove_spaces_and_ret(s):
    s = s.replace('\n', '')
    return re.sub(r'\s+', ' ', s)

def get_fac(group_n):
    return faculty[int(group_n[0])]

def get_current_week(div_weeks):
    print(type(div_weeks))
    week_info = div_weeks.find('li', {'class' : 'current'}).findAll('div')
    return {'week_info' :{
        'ood': remove_spaces_and_ret(week_info[0].text),
        'start_with': remove_spaces_and_ret(week_info[1].text)
    }}





def get_timetable(tt):
    rez = {}
    thead = tt.find('thead').findAll('th')
    for i, t in enumerate(thead):
        t = t.text
        t = remove_spaces_and_ret(t)
        if i != 0:
            rez[i] = ({'date': t, 'day': days[i]})
            rez[i]['subjects_list'] = []
    
    del thead

    tbody = tt.find('tbody')
    for l in range(1, 7):
        cl = f'lesson_{l}'
        row = tbody.find('tr', {'class': cl})
        time = row.find('th', {'class': 'time'}).text
        time = remove_spaces_and_ret(time)
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

        

    



def main():
    group_num = sys.argv[1]
    group_fuc = get_fac(group_num)
    rez = {}
    week_num = ''

    tt_url = f'https://timetable.tusur.ru/faculties/{group_fuc}/groups/{group_num}?week_id={week_num}'


    resp = requests.get(tt_url)

    root_html = bs(resp.text, 'lxml').html

    week_slider = root_html.findAll('div', attrs={'class': 'col-md-12'})[1]
    rez.update(get_current_week(week_slider))
    

    week_timetable = root_html.findAll('div', attrs={'class': 'col-md-12'})[3].find('div', {'class': 'table-responsive'})

    
    rez.update(get_timetable(week_timetable))

    
    with open(f'out/{group_num}.json', 'w', encoding='utf-8') as fout:
        # fout.write(week_timetable.prettify())
        # pass
        json.dump(rez, fout, indent=4, ensure_ascii=False)
        # print(rez)



if __name__ == "__main__":
    main()