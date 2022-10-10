from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import lego_elements as l
import uuid
import os
import json
import urllib.request


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
            
            element = self.find_element_soup(element_name)
            
            if (element == None and appear == 'disappear') or (element != None and appear == 'appear'):
                return True
            
            if time.time() > starting_time + period:
                if print_warning:
                    print(f'waited {period} seconds for element {element_name} to {appear}. But it never did.')
                return False
    
    
    
    def wait_for_then_click(self, buttons, period = 10, print_warning = True):
            
        for button_name in buttons:
            
            if self.wait_for(button_name, period = period, print_warning = print_warning):
                self.click_button(button_name)
    
    
    
    def scroll_to_bottom(self, bottom_element_name, condition_element_name, condition):
        
        while not condition(self.find_element_soup(condition_element_name)):
            
            self.driver.execute_script("arguments[0].scrollIntoView();", self.find_element(bottom_element_name))
    
    
    
    def harvest_links(self, element_name, condition):
        
        link_elements = self.find_element_soup(element_name).find_all(condition)
        
        return [link_element.get('href') for link_element in link_elements]
    
    
    
    def harvest_image_sources(self, element_list, condition = lambda tag : tag.name == 'img'):
        
        picture_elements = [self.find_element_soup(element_name).find_all(condition) for element_name in element_list]
        picture_elements_flattened = [picture_element for sublist in picture_elements for picture_element in sublist]
        
        return [picture_element.get('src').split('?')[0] for picture_element in picture_elements_flattened]
    
    
    
    def harvest_text_from_elements(self, element_list):
        
        get_text_of = lambda element_name : self.find_element_soup(element_name).get_text(separator = '¬')
        
        return {element_name : get_text_of(element_name) for element_name in element_list}
    
    
    
    def store_data(self, data):
        
        path = os.path.join('raw_data', data['ID'])
        
        try:
            os.mkdir(path)
        except:
            print('Storing data in an ID that already exists!')
        
        with open(f'{path}\data.json', 'w', encoding = 'utf-8') as file:
            json.dump(data, file)
    
    
    
    def filter_elements(self, filters):
        
        check = lambda e : 'filters' in self.elements[e].keys() and (set(filters) & self.elements[e]['filters'])
        
        return([element_name for element_name in self.elements.keys() if check(element_name)])
    
    
    
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
            page_html = self.driver.execute_script("return document.documentElement.outerHTML;")
            return BeautifulSoup(page_html, 'html.parser')
        
        element = self.elements[element_name]
        parent = self.find_element_soup(element['dependency'])

        return parent.find(element['condition'])
    
    
    derive_xpath = lambda self, element_name : self.build_xpath(self.find_element_soup(element_name))
    
    
    find_element = lambda self, element_name : self.driver.find_element(By.XPATH, self.derive_xpath(element_name))





class LegoScraper(Scraper):
    
    
    def __init__(self):
        super().__init__(l.front_page_link, 'front_page')
        self.elements = l.dictionary
        self.setup()
        #self.links = self.get_lego_links()
    
    
    
    def setup(self):

        self.wait_for('age_check_overlay')
        self.wait_for_then_click(['age_check_button', 'cookie_accept_button'])
    
    
    
    def get_lego_links(self):
        
        details_page_links = []
        for product_list_link in l.product_list_links:
            
            self.navigate(product_list_link, 'product_list')
            self.clear_survey_window()
            self.wait_for_then_click(['sets_checkbox', 'show_all_button'])
            
            self.wait_for('page_bottom_post_show_all')
            condition = lambda element : element.get_text().split()[1] == element.get_text().split()[-1]
            #above condition checks if x == y in "showing x of y text" element.
            self.scroll_to_bottom('page_bottom_post_show_all', 'showing_x_of_y_text', condition)
            
            condition = lambda element : element.has_attr('data-test') and element['data-test'] == 'product-leaf-title-link'
            details_page_links = details_page_links + self.harvest_links('page_info', condition)
        
        return(details_page_links)
    
    
    
    def collect_product_data(self, link, download_pics = False):

        product_id = link.split('-')[-1]
        self.navigate(link, f'{product_id}_details_page')
        self.clear_survey_window()
    
        imgs = lego.harvest_image_sources(self.filter_elements(['image_elements']))
        text = lego.harvest_text_from_elements(self.filter_elements(['text_elements']))
        spl_text = {element_name : element_text.split('¬') for element_name, element_text in text.items()}
        data = {**text, 'img_links' : imgs, 'UUID' : str(uuid.uuid4())}
        
        key_mapping = lambda schema: spl_text[schema[0]][schema[1]] if len(schema) > 1 else data[schema[0]]
        condition = lambda schema : schema[0] not in l.data_restrictions.keys() or l.data_restrictions[schema[0]](spl_text[schema[0]])
        formatted_data = {key : key_mapping(schema) if condition(schema) else None for key, schema in l.data_schema.items()}
        
        self.store_data(formatted_data)
        if download_pics:
            self.store_image_data(formatted_data)
        return formatted_data
    
    
    
    def collect_products_data(self, links, download_pics = False):
        
        for link in links:
            self.collect_product_data(link, download_pics)
    
    
    
    def store_image_data(self, data):
        
        for link in data['Image Links']:
            
            link_ending = link.split('/')[-1].split('_')
            
            if len(link_ending) == 1:
                category = 'main_picture'
            else:
                link_ending[-1] = ''.join([i for i in link_ending[-1] if not i.isdigit()])
                category = '_'.join(link_ending[1:]).split('.')[0]
            
            path = os.path.join('raw_data', data['ID'], 'pictures', category)
            if not os.path.isdir(path):
                os.makedirs(path)
            
            filepath = os.path.join(path, link.split('/')[-1])
            urllib.request.urlretrieve(link, filepath)
    
    
    
    def clear_survey_window(self):
            if self.wait_for('survey_window', period = 5, print_warning = False):
                self.click_button('survey_window_no')





if __name__ == '__main__':
    
    lego = LegoScraper()
    product_data = lego.collect_products_data(['https://www.lego.com/en-gb/product/tony-stark-s-sakaarian-iron-man-76194', \
        'https://www.lego.com/en-gb/product/shuri-s-sunbird-76211'], download_pics = True)