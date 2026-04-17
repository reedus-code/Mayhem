from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import readchar


error_code = []
tinka_url = 'https://resultados.latinka.com.pe/i.do?m=historico&t=0&s=41'
data_tinka = {'id_tinka': [],
              'date': [],
              'lucky_numbers': [],
              'check' : [],
              'b_one' : [],
              'b_two' : [],
              'b_three' : [],
              'b_four' : [],
              'b_five' : [],
              'b_six' : [],
              'yapa': [],
              'sio_si': []}


def get_data (url):
    session = HTMLSession()
    tinka_web = session.get(url)
    table_tinka = tinka_web.html.find('#historico', first=True)
    soup = BeautifulSoup(table_tinka.html, 'html.parser')
    rows = soup.find_all('tr')

    for row in rows:
        contents = row.find_all('td')

        date_text = contents[0].get_text(strip=True)
        data_tinka['date'].append(date_text)
        sorteo_text = contents[1].get_text(strip=True)
        data_tinka['id_tinka'].append(sorteo_text)
        bolillas_text = contents[2].get_text(strip=True)
        data_tinka['lucky_numbers'].append(bolillas_text)
        yapa_text = contents[3].get_text(strip=True)
        data_tinka['yapa'].append(yapa_text)
        suerte_text = contents[4].get_text(strip=True)
        data_tinka['sio_si'].append(suerte_text)
    return data_tinka


def show_info_tinka(df):
    print(df.head())
    #print(df.info())
    df_repeat_numb = df[df['check'].duplicated()]
    duplicate_list = [df[ticket == df['check']] for ticket in df_repeat_numb['check']]
    print('\n\x1b[3m\x1b[31mLista jugadas repetidas\x1b[0m\n')
    for item in duplicate_list:
        print(item)
    print('\n\x1b[3m\x1b[33m[PRESS ANY KEY TO CONTINUE]\x1b[0m')
    readchar.readchar()


def save_as_cvs(variable):
    df = pd.DataFrame(variable)

    df.loc[df['yapa'] == '', 'yapa'] = '0'
    df['yapa'] =  df['yapa'].apply(int)
    df['date'] = pd.to_datetime(df['date'], dayfirst=True)

    csv_path = Path('la_tinka.csv')
    df.to_csv(csv_path, index=False)
    print('\x1b[3m\x1b[31m[ARCHIVO GUARDADO]\x1b[0m\n'
          '\x1b[43mla_tinka.csv\x1b[0m\n\n')
    show_info_tinka(df)


def check_csv():
    try:
        csv_path = Path('la_tinka.csv')
        df = pd.read_csv(csv_path)
        show_info_tinka(df)
        exit()

    except FileNotFoundError:
        print('\x1b[3m\x1b[31m[Archivo no encontrado]\x1b[0m\n'
              '\x1b[43mFile not fount: la_tinka.csv\x1b[0m\n')
        error_code.append('1A')


def check_data (error):
    #NO CSV
    if '1A' in error:
        print('\x1b[3m\x1b[31m[DESCARGANDO DATA...]\x1b[0m')
        la_tinka = get_data(tinka_url)
        la_tinka = tinka_legacy(la_tinka)
        return la_tinka
        


def tinka_legacy(data):
    data['sio_si'] = [item.replace(' ', ' - ') for item in data['sio_si']]
    data['lucky_numbers'] = [item.replace(' ', ' - ') for item in data['lucky_numbers']]
    for item in data['lucky_numbers']:
        set_to_numb = item.split(' - ')
        data['b_one'].append(int(set_to_numb[0]))
        data['b_two'].append(int(set_to_numb[1]))
        data['b_three'].append(int(set_to_numb[2]))
        data['b_four'].append(int(set_to_numb[3]))
        data['b_five'].append(int(set_to_numb[4]))
        data['b_six'].append(int(set_to_numb[5]))

        data['check'].append(', '.join(sorted(set_to_numb)))

    return data


def main ():
    check_csv()
    la_tinka = check_data(error_code)
    save_as_cvs(la_tinka)


if __name__ == '__main__':
    main()