import datetime
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
from mechanize import Browser

class BetFair():
    
    
    def __init__(self, url, filename, sample_time, n_attempts=2):
        self.filename = filename
        self.sample_time = sample_time
        self.n_attempts = n_attempts
        sleep_time = 5
        self.url = url
        self.br = Browser()
        
        while(True):
            attempt = 0
            for attempt in range(n_attempts):
                try:
                    self._load_page()
                    self.write_games_odds()
                    break
                except:
                    print('Erro!')
                    time.sleep(sleep_time)
            
            time.sleep(self.sample_time-attempt*sleep_time)
            
        
    def _load_page(self):
        self.time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        page_content = self.br.open(self.url).read()
        page = BeautifulSoup(page_content,"lxml")
        page = page.find_all('div', class_='content-multipick')
        self.page = page[0].find_all('div', class_='details-market market-3-runners')
        print('start betfair' + self.time)
        
    def _get_games_odds(self, pg):
        
        #TODO: tirar a porra desse slice 
        start = str(pg.find_all('a')[0]).find('data-galabel')
        end = str(pg.find_all('a')[0]).find('data-loader')
        teams = str(pg.find_all('a')[0])[start+14:end-11].split(' x ')
        team1 = teams[0]
        team2 = teams[1]

        x1 = str(pg.find_all('a')[1].find().get_text().replace('\n', ''))
        x2 = str(pg.find_all('a')[2].find().get_text().replace('\n', ''))
        x3 = str(pg.find_all('a')[3].find().get_text().replace('\n', ''))

        return [team1, team2, x1, x2, x3]
        
    def write_games_odds(self):
        for pg in self.page:
            self._write_file(self._get_games_odds(pg))

    def _write_file(self, line):
        try:
            with open(self.filename, "a") as f:
                f.write('\n'+self.time)
                for x in line:
                    f.write(';'+ x)
        except:
            print('Criando arquivo: ' + self.filename)
            with open(self.filename, "w") as f:
                f.write('\n'+self.time)
                for x in line:
                    f.write(';'+ x)

if __name__ == '__main__':
    TODAY_STR = datetime.now().strftime('%Y%m%d')
    url = 'https://www.betfair.com/sport/football/uefa-liga-dos-campe%C3%B5es/228'
    BetFair(url, 'betfair{}champions.txt'.format(TODAY_STR), 60)                
