from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import requests


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
                
                if time.time() > starting_time + 10:
                    print(f"Failed to press button (identified by {identification}) with identification {button}")
                    break
          
                

    def remove_cookies(self, identification = 'XPATH'):
        self.click_buttons(self.cookie_buttons, identification)
    
    
    
    def scroll_to_bottom(self):
        
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:

            self.driver.execute_script("window.scrollTo(100, document.body.scrollHeight);")
            time.sleep(1)

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                break
            last_height = new_height
            
        

if __name__ == '__main__':
    
    lego = Scraper('https://www.lego.com/en-gb')
    
    lego.cookie_buttons = ['//*[@id="__next"]/div[5]/div/div/div[1]/div[1]/div/button',
                           '/html/body/div[6]/div/aside/div/div/div[3]/div[1]/button[1]']
    lego.remove_cookies()
    
    lego.driver.get('https://www.lego.com/en-gb/categories/age-1-plus-years')
    buttons = ['//*[@id="product-facet-productType-accordion-content"]/div/div/ul/li[1]/label/div',
               '/html/body/div[1]/main/div/div[4]/div/div/section/div/div[2]/div/div/a']
    lego.click_buttons(buttons)
    lego.scroll_to_bottom()
    print('done')
    
    #To be removed soon --
    
    # //*[@id="bltc6cdf6e15ea6c848"]/section/div/div[2]/div/div/a
    
    # [@id="bltb4ff2489704d2385"]//*[@id="bltb4ff2489704d2385"]/section/div/div[2]/div/div
    
    # //*[@id="blt0723e5915b29f00d"]/section/div/div[2]/div/div
    
    # //*[@id="blt0723e5915b29f00d"]/section/div/div[2]/div

    
    # ProductListingsstyles__ProductsWrapper-sc-1taio5c-2 dFBaNn
    
    # ProductListingsstyles__ProductsWrapper-sc-1taio5c-2 dFBaNn
    
    # ProductListingsstyles__ProductsWrapper-sc-1taio5c-2 dFBaNn
    
    
    
    # ProductListingsstyles__ProductsWrapper-sc-1taio5c-2 dFBaNn
    
    # LinksNextstyles__AnchorButton-sc-1sxojvh-1 kARNPN Paginationstyles__ShowAllLink-npbsev-13 iWkTte