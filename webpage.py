from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import lego_elements as l
import uuid


class Scraper:
    
    
    def __init__(self, URL, webpage_name):
        
        self.driver = webdriver.Chrome()
        self.elements = dict()
        self.driver.get(URL)
        self.webpage = webpage_name
    
    
    
    def navigate(self, URL, webpage_name):
        
        self.driver.get(URL)
        self.webpage = webpage_name
    
    
    
    def click_button(self, button_name):
        
        try:
            self.find_element(button_name).click()
        except:
            print(f'failed to press button {button_name} on page {self.webpage}.')
            
        time.sleep(1)
    
    
    
    def wait_for(self, element_name, appear = 'appear', period = 10, print_warning = True):
        
        starting_time = time.time()
        
        while True:
            
            if (self.find_element_soup(element_name) == None) and (appear == 'disappear'):
                return True
            if (self.find_element_soup(element_name) != None) and (appear == 'appear'):
                return True
            
            if time.time() > starting_time + period:
                if print_warning:
                    print(f"waited {period} seconds for element {element_name} to {appear}. But it never did.")
                return False
    
    
    
    def wait_for_then_click(self, buttons, period = 10, print_warning = True):
            
        for button_name in buttons:
            if self.wait_for(button_name, period = period, print_warning = print_warning):
                self.click_button(button_name)
    
    
    
    def scroll_to_bottom(self, bottom_element_name, condition_element_name, condition):
        
        while not condition(self.find_element_soup(condition_element_name)):
            self.driver.execute_script("arguments[0].scrollIntoView();", self.find_element(bottom_element_name))
    
    
    
    def harvest_links(self, element_name, condition):
        
        element = self.find_element_soup(element_name)
        links = []
        
        for link_element in element.find_all(condition):
            links.append(link_element.get('href'))
        
        return links
    
    
    
    def harvest_image_sources(self, element_name, condition = lambda tag : tag.name == 'img'):
        
        print(self.elements[element_name])
        element = self.find_element_soup(element_name)
        src_names = []
        
        for picture_element in element.find_all(condition):
            src_names.append(picture_element.get('src').split('?')[0])
        
        return src_names
    
    
    
    def harvest_text_from_elements(self, element_list):
        
        text = dict()
        
        for element_name in element_list:
            element = self.find_element_soup(element_name)
            text[element_name] = element.get_text(separator = '¬')
        
        return text
    
    
    
    def build_xpath(self, element):
    
        components = []
        
        for parent in element.parents:
            
            siblings = parent.find_all(element.name, recursive = False)
            
            if len(siblings) == 1:
                components.append(element.name)
                
            else:
                for index, sibling in enumerate(siblings, 1):
                    if sibling is element:
                        components.append(f'{element.name}[{str(index)}]')
                        
            element = parent
        
        components.reverse()
        return('/' + '/'.join(components))
    
    
    
    def find_element_soup(self, element_name):
        
        if element_name == 'webpage':
            return BeautifulSoup(self.driver.execute_script("return document.documentElement.outerHTML;"), 'html.parser')
        
        element = self.elements[element_name]
        parent = self.find_element_soup(element['dependency'])

        return parent.find(element['condition'])
    
    derive_xpath = lambda self, element_name : self.build_xpath(self.find_element_soup(element_name))
    
    find_element = lambda self, element_name : self.driver.find_element(By.XPATH, self.derive_xpath(element_name))





class LegoScraper(Scraper):
    
    
    def __init__(self):
        super().__init___(l.front_page_link, 'front_page')
        self.elements = l.dictionary
        self.setup()
        #self.links = self.get_lego_links()
    
    
    
    def setup(self):

        lego.wait_for('age_check_overlay')
        lego.click_buttons(['age_check_button', 'cookie_accept_button'])
    
    
    
    def get_lego_links(self):
        
        details_page_links = []
        for product_list_link in l.product_list_links:
            
            self.navigate(product_list_link, 'product_list')
            
            if self.wait_for('survey_window', period = 5, print_warning = False):
                self.click_button('survey_window_no')
            
            self.click_button('sets_checkbox')
            self.wait_for('show_all_button')
            self.click_button('show_all_button')
            
            self.wait_for('page_bottom_post_show_all')
            condition = lambda element : element.get_text().split()[1] == element.get_text().split()[-1]
            #above condition checks if x == y in "showing_x_of_y_text" element.
            self.scroll_to_bottom('page_bottom_post_show_all', 'showing_x_of_y_text', condition)
            
            condition = lambda element : element.has_attr('data-test') and element['data-test'] == 'product-leaf-title-link'
            #above condition specifies those elements which have a text link.
            details_page_links = details_page_links + self.harvest_links('page_info', condition)
        
        return(details_page_links)
    
    
    
    def expand_lego_data(self, text, img_links):
        
        
        item_stats = text['item_stats'].split('¬')
        item_rating = text['item_rating'].split('¬')
        item_price = text['item_price'].split('¬')
        
        return {'ID' : item_stats[6],
                'Name' : item_rating[0],
                'Price' : item_price[1],
                'Age' : item_stats[0],
                'Pieces' : item_stats[2],
                'Average Rating' : item_rating[1],
                'Number of Ratings' : item_rating[3],
                'Description' : text['item_description'],
                'Image Links' : img_links,
                'UUID' : uuid.uuid4()
        }
    
    
    
    def store_lego_data(self):
        pass

if __name__ == '__main__':
    
    setup_lego()
    lego.navigate('https://www.lego.com/en-gb/product/90-years-of-play-11021', 'details_page')
    
    page = lego.find_element_soup('webpage')
    
    text = []
    counter = 0
    
    baddies = ['All rights reserved', 'Skip to main content', 'Play Zone', 'ShopDiscoverHelp', 'Sets by themeAgesPrice']
    
    if lego.wait_for('survey_window', period = 5, print_warning = False):
        lego.click_button('survey_window_no')
    
    imgs = lego.harvest_image_sources('item_pictures')
    text = lego.harvest_text_from_elements(['item_description', 'item_stats', 'item_rating', 'item_price'])
    product_data = expand_lego_text(text, imgs)
    print(product_data)

    # imgs = lego.harvest_image_sources('item_pictures')
    # for img in imgs:
    #     print(img)
    
    # for element in page.find_all():
    #     check = sum([element.get_text().count(baddie) for baddie in baddies])
    #     if check != 0 or element.get_text() == '':
    #         continue
    #     text.append((lego.build_xpath(element), element.get_text(separator = '¬')))
    #     counter += 1
    #     if counter == 500:
    #         break
    
    # f = open('output.txt', 'w', encoding = 'utf-8')
    # for x in set(text):
    #     f.write(f'\n{x}')
    # f.close()