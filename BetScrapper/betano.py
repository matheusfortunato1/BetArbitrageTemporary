import datetime
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime

class Betano():
    
    
    def __init__(self, url, filename, sample_time, n_attempts=2):
        self.filename = filename
        self.sample_time = sample_time
        self.n_attempts = n_attempts
        self.sleep_time = sample_time/5
        self.url = url
        self.driver = self._init_chromium_driver()
        
#         self._load_page()
        while(True):
            attempt = 0
            for attempt in range(n_attempts):
                try:
                    self._load_page()
                    self.write_games_odds()
                    break
                except:
                    print('Erro!')
                    time.sleep(self.sleep_time)
            time.sleep(0.5*self.sample_time-attempt*self.sleep_time)
            
    def _init_chromium_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        return webdriver.Chrome(options=options)
            
    def _load_page(self):
        print('betano - start...' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.driver.get(self.url)
        time.sleep(self.sleep_time)
        # Fucking sleep cause shit download speed
        page_source = self.driver.page_source
        time.sleep(self.sleep_time)
        self.page = BeautifulSoup(page_source, "lxml")
        
    def _write_odds(self):
        with open(self.filename, "a") as f:
            for pg in self.page.find_all('td', class_='table__markets__market'):
                for odd in pg.find_all('span', class_='selections__selection__odd'):
                    f.write(odd.getText()+';')
            f.write('\n')
    
    def _write_teams(self):
        with open(self.filename, "a") as f:
            f.write(self.time+';')
            for pg in self.page.find_all('th', class_='events-list__grid__info'):
                for team in pg.find_all('span'):
                    f.write(team.getText().strip()+';')
                    
    def write_games_odds(self):
        self._write_teams()
        self._write_odds()

if __name__ == '__main__':
    TODAY_STR = datetime.now().strftime('%Y%m%d')
    url = 'https://br.betano.com/sport/futebol/liga-dos-campeoes/liga-dos-campeoes-jogos/182748/'
    Betano(url, 'betano{}.txt'.format(TODAY_STR), 60)
