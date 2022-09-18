from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select


class Scraper:
    
    
    def __init__(self, URL):
        

        self.driver = webdriver.Chrome()
        self.driver.get(URL)
        self.cookie_buttons = []
    
    
    
    def click_button(self, identifier, identification = 'XPATH'):
        exec('self.driver.find_element(By.' + identification + ', \'' + identifier+ '\').click()')
        time.sleep(1)
    
    
    
    def click_buttons(self, buttons, identification = 'XPATH'):
        
        for button in buttons:
            
            starting_time = time.time()
            
            while True:
                
                try:
                    self.click_button(button, identification)
                    break
                except:
                    pass
          
                

    def remove_cookies(self, identification = 'XPATH'):
        self.click_buttons(self.cookie_buttons, identification)
    
    
    
    def scroll_to_bottom(self):
        
        while True:

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            
        

if __name__ == '__main__':
    
    lego = Scraper('https://www.lego.com/en-gb')
    
    lego.cookie_buttons = ['//*[@id="__next"]/div[5]/div/div/div[1]/div[1]/div/button',
                           '/html/body/div[6]/div/aside/div/div/div[3]/div[1]/button[1]']
    lego.remove_cookies()