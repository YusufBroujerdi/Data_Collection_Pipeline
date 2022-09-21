from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import lego_elements as l


class Scraper:
    
    
    def __init__(self, URL, webpage_name):
        
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        self.driver = webdriver.Chrome(chrome_options = options)
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
    
    
    
    def click_buttons(self, buttons):
        
        for button_name in buttons:
            self.click_button(button_name)
    
    
    
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
    
    
    
    def scroll_to_bottom(self, bottom_element_name, condition_element_name, condition):
        
        while not condition(self.find_element_soup(condition_element_name)):
            self.driver.execute_script("arguments[0].scrollIntoView();", self.find_element(bottom_element_name))
    
    
    
    def harvest_links(self, element_name, condition):
        
        element = self.find_element_soup(element_name)
        links = []
        
        for link_element in element.find_all(condition):
            links.append(link_element.get('href'))
        
        return links
    
    
    
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
        
        element = self.elements[element_name]
        
        if element['dependency'] == self.webpage:
            parent = BeautifulSoup(self.driver.execute_script("return document.documentElement.outerHTML;"), 'html.parser')
        else:
            parent = self.find_element_soup(element['dependency'])
        
        return parent.find(element['condition'])
    
    derive_xpath = lambda self, element_name : self.build_xpath(self.find_element_soup(element_name))
    
    find_element = lambda self, element_name : self.driver.find_element(By.XPATH, self.derive_xpath(element_name))





if __name__ == '__main__':
    
    lego = Scraper(l.front_page_link, 'front_page')
    lego.elements = l.dictionary
    lego.wait_for('age_check_overlay')
    lego.click_buttons(['age_check_button', 'cookie_accept_button'])
    
    details_page_links = []
    for product_list_link in l.product_list_links:
        
        lego.navigate(product_list_link, 'product_list')
        if lego.wait_for('survey_window', period = 5, print_warning = False):
            lego.click_button('survey_window_no')
        lego.click_button('sets_checkbox')
        lego.wait_for('show_all_button')
        lego.click_button('show_all_button')
        
        lego.wait_for('page_bottom_post_show_all')
        condition = lambda element : element.get_text().split()[1] == element.get_text().split()[-1]
        lego.scroll_to_bottom('page_bottom_post_show_all', 'showing_x_of_y_text', condition)
        
        condition = lambda tag : tag.has_attr('data-test') and tag['data-test'] == 'product-leaf-title-link'
        details_page_links = details_page_links + lego.harvest_links('page_info', condition)
    
    print(details_page_links)