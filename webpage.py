from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
import json
import lego_elements as l
import os
import time
import urllib.request
import uuid

class SeleniumElement:
    pass

class SoupElement:
    pass




class Scraper:
    
    
    def __init__(self, URL : str):
        
        self.driver = webdriver.Chrome()
        self.elements = dict()
        self.data_restrictions = dict()
        self.data_schema = dict()
        self.driver.get(URL)
    
    
    
    def navigate(self, URL : str):
        '''Navigate driver to webpage with the given URL.'''
        
        self.driver.get(URL)
    
    
    
    def click_button(self, button_name : str):
        '''Click button with the given name from the elements dictionary.'''
        
        try:
            self.__find_element(button_name).click()
        except:
            print(f'failed to press button {button_name}.')
            
        time.sleep(1)
    
    
    
    def wait_for(self, element_name : str, appear : str = 'appear', seconds_to_wait : int = 10, print_warning : bool = True) -> bool:
        '''Wait "seconds_to_wait" seconds for the given element to appear/disappear.'''
        
        starting_time = time.time()
        
        while True:
            
            element = self.find_element_soup(element_name)
            
            if (element == None and appear == 'disappear') or (element != None and appear == 'appear'):
                return True
            
            if time.time() > starting_time + seconds_to_wait:
                if print_warning:
                    print(f'waited {seconds_to_wait} seconds for element {element_name} to {appear}. But it never did.')
                return False
    
    
    
    def wait_for_then_click(self, buttons : list, seconds_to_wait : int = 10, print_warning : bool = True):
        '''Wait "seconds_to_wait" seconds for the given element, then click it.'''
        for button_name in buttons:
            
            if self.wait_for(button_name, seconds_to_wait = seconds_to_wait, print_warning = print_warning):
                self.click_button(button_name)
    
    
    
    def scroll_to(self, bottom_element_name : str, condition_element_name : str, condition : function):
        '''Scroll to the "bottom_element" until the "condition_element" no longer satisfies the "condition".'''
        
        while not condition(self.find_element_soup(condition_element_name)):
            
            self.driver.execute_script('arguments[0].scrollIntoView();', self.__find_element(bottom_element_name))
    
    
    
    def collect_links(self, element_name : str, condition : function) -> list:
        '''Collect links from every child element of "element" that satisfies the "condition".'''
        link_elements = self.find_element_soup(element_name).find_all(condition)
        
        return [link_element.get('href') for link_element in link_elements]
    
    
    
    def collect_image_sources(self, elements : list, condition : function = lambda tag : tag.name == 'img') -> list:
        '''Collect image sources from every element in the list of "elements" that satisfies the "condition".'''
        picture_elements = [self.find_element_soup(element_name).find_all(condition) for element_name in elements]
        picture_elements_flattened = [picture_element for sublist in picture_elements for picture_element in sublist]
        
        return [picture_element.get('src').split('?')[0] for picture_element in picture_elements_flattened]
    
    
    
    def collect_text_from_elements(self, elements : list) -> dict:
        '''Collect text from every element in the list of "elements" and return a dictionary.'''
        get_text_of = lambda element_name : self.find_element_soup(element_name).get_text(separator = '¬')
        
        return {element_name : get_text_of(element_name) for element_name in elements}
    
    
    
    def __collect_page_data(self) -> dict:
        '''Collect all the text and images from the page and return a dictionary.'''
        imgs = self.collect_image_sources(self.filter_elements(['image_elements']))
        text = self.collect_text_from_elements(self.filter_elements(['text_elements']))
        data = {**text, 'img_links' : imgs, 'UUID' : str(uuid.uuid4())}
        
        return(data)
    
    
    
    def __format_data(self, data : dict) -> dict:
        '''Format the data dictionary produced by "__collect_page_data", using the layout in "data_schema" and respecting the conditions given in "data_restrictions".'''
        key_mapping = lambda schema: schema['map'](data[schema['element']]) if 'map' in schema.keys() else data[schema['element']]
        
        data_restriction_check = lambda element : element not in self.data_restrictions.keys() or self.data_restrictions[element](data[element])
        
        formatted_data = {key : key_mapping(schema) if data_restriction_check(schema['element']) else None for key, schema in self.data_schema.items()}
        
        return(formatted_data)
    
    
    
    def collect_product_data(self, link : str, download_pics : bool = False) -> dict:
        '''Collect, format and store the data from a link.'''
        self.navigate(link)
        
        data = self.__collect_page_data()
        
        formatted_data = self.__format_data(data)
        
        self.__store_text_data(formatted_data)
        if download_pics:
            self.__store_image_data(formatted_data)
        return formatted_data
    
    
    
    def collect_products_data(self, links : list, download_pics : bool = False):
        '''Collect, format and store the data from a list of links.'''
        for link in links:
            self.collect_product_data(link, download_pics)
    
    
    
    def __store_text_data(self, data : dict):
        '''Store the text data formatted with __format_data.'''
        path = os.path.join('raw_data', data['ID'])
        
        try:
            os.mkdir(path)
        except:
            print('Storing data in an ID that already exists!')
        
        with open(f'{path}\data.json', 'w', encoding = 'utf-8') as file:
            json.dump(data, file)
    
    
    
    def __store_image_data(self, data : dict):
        '''Store the image data formatted with __format_data'''
        for link in data['Image Links']:
            
            category = self.derive_image_category(link)
            
            path = os.path.join('raw_data', data['ID'], 'pictures', category)
            if not os.path.isdir(path):
                os.makedirs(path)
            
            filepath = os.path.join(path, link.split('/')[-1])
            urllib.request.urlretrieve(link, filepath)
    
    
    def derive_image_category(self, link : str) -> str:
        '''Deduce the folder category of an image from its link. (LegoScraper has a more developed version of this method.)'''
        return 'all'
    
    
    
    def filter_elements(self, filters : set) -> list:
        '''Filter the elements of the elements dictionary by the given filters.'''
        check = lambda element_name : 'filters' in self.elements[element_name].keys() and (set(filters) & self.elements[element_name]['filters'])
        
        return([element_name for element_name in self.elements.keys() if check(element_name)])
    
    
    
    def derive_xpath(self, element : SoupElement) -> str:
        '''Deduce the xpath of a SoupElement.'''
        components = [] #The components list will eventually list out all the components that build up the xpath.
        
        for parent in element.parents:
            
            siblings = parent.find_all(element.name, recursive = False)
            
            #Component is appended as simply "element.name" if it has no siblings with the same name, else "element.name[n]".
            if len(siblings) == 1:
                components.append(element.name) 
            else:
                components += [f'{element.name}[{str(index)}]' for index, sibling in enumerate(siblings, 1) if sibling is element]
            
            element = parent
        
        components.reverse()
        return('/' + '/'.join(components))
    
    
    
    def find_element_soup(self, element_name : str) -> SoupElement:
        '''Return the "Soup-form" of an element, using its "element_name" given in the elements dictionary.'''
        if element_name == 'webpage':
            page_html = self.driver.execute_script('return document.documentElement.outerHTML;')
            return BeautifulSoup(page_html, 'html.parser')
        
        element = self.elements[element_name]
        parent = self.find_element_soup(element['dependency'])

        return parent.find(element['condition'])
    
    
    
    def __find_element(self, element_name : str) -> SeleniumElement:
        '''Return the "Selenium-form" of an element, using its "element_name" given in the elements dictionary.'''
        xpath = self.derive_xpath(self.find_element_soup(element_name))
        self.driver.find_element(By.XPATH, xpath)





class LegoScraper(Scraper):
    
    
    def __init__(self):
        
        super().__init__(l.front_page_link)
        self.elements = l.dictionary
        self.data_restrictions = l.data_restrictions
        self.data_schema = l.data_schema
        self.__setup_front_page()
        #self.links = self.collect_lego_set_links()
    

    
    def __clear_survey_window(self):
        '''Clear lego survey window if it appears.'''
        if self.wait_for('survey_window', seconds_to_wait = 5, print_warning = False):
            self.click_button('survey_window_no')   
    
    
    
    def navigate(self, URL):
        '''Navigate to the URL, and clear the lego survey window if it appears.'''
        super().navigate(URL)
        self.__clear_survey_window()
    
    
    
    def __setup_front_page(self):
        '''Clear the windows that appear on the front page.'''
        self.wait_for('age_check_overlay')
        self.wait_for_then_click(['age_check_button', 'cookie_accept_button'])
    
    
    
    def __scroll_until_all_products_appear(self):
        '''Scroll down the page until all products have loaded.'''
        self.wait_for('page_bottom_post_show_all')
        are_all_products_shown = lambda element : element.get_text().split()[1] == element.get_text().split()[-1]
        self.scroll_to('page_bottom_post_show_all', 'showing_x_of_y_text', are_all_products_shown)
    
    
    
    def collect_lego_set_links(self) -> list:
        '''Collect all the links on the product_list pages for lego sets.'''
        details_page_links = []
        for product_list_link in l.product_list_links:
            
            self.navigate(product_list_link, 'product_list')
            
            self.wait_for_then_click(['sets_checkbox', 'show_all_button'])
            
            self.__scroll_until_all_products_appear()
            
            condition = lambda element : element.has_attr('data-test') and element['data-test'] == 'product-leaf-title-link'
            details_page_links = details_page_links + self.collect_links('page_info', condition)
        
        return(details_page_links)
    
    
    
    def derive_image_category(self, link : str) -> str:
        '''Deduce the folder category of an image from its link.'''
        link_ending = link.split('/')[-1].split('_')
            
        if len(link_ending) == 1:
            category = 'main_picture'
        else:
            link_ending[-1] = ''.join([char for char in link_ending[-1] if not char.isdigit()])
            category = '_'.join(link_ending[1:]).split('.')[0]
        
        return category





if __name__ == '__main__':
    
    lego = LegoScraper()
    product_data = lego.collect_products_data(['https://www.lego.com/en-gb/product/tony-stark-s-sakaarian-iron-man-76194', \
        'https://www.lego.com/en-gb/product/shuri-s-sunbird-76211'], download_pics = True)