import datetime
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime

class SportingBet():
    
    
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
                    print('Página carregou')
                    self.write_games_odds()
                    print('Foi escrito')
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
        print('start...' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.driver.get(self.url)
        time.sleep(self.sleep_time)
        print('Get url ok ')
        # Fucking sleep cause shit download speed
        page_source = self.driver.page_source
        time.sleep(self.sleep_time)
        self.page = BeautifulSoup(page_source, "lxml")
        
    def _write_odds(self):
        with open(self.filename, "a") as f:
            for pg in self.page.find_all('div', class_='option option-indicator ng-star-inserted'):
                f.write(str(pg.getText())+';')
            f.write('\n')
    
    def _write_teams(self):
        with open(self.filename, "a") as f:
            print('Entrou em write teams')
            f.write(self.time+';')
            for pg in self.page.find_all('div', class_='participant'):
                print(str(pg.getText().strip())+';')
                f.write(str(pg.getText().strip())+';')
            
    def write_games_odds(self):
        self._write_teams()
        self._write_odds()

if __name__ == '__main__':
    TODAY_STR = datetime.now().strftime('%Y%m%d')
    url = 'https://sports.sportingbet.com/pt-br/sports/futebol-4/aposta/europa-7/liga-dos-campe%C3%B5es-0:3'
    SportingBet(url, 'sportingbet{}champions.txt'.format(TODAY_STR), 60)
