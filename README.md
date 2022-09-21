# Data_Collection_Pipeline

> The Goal of this project is to harvest data from lego.

## Milestones 1-2

- I'm making use of the packages BeautifulSoup and Selenium to interact with the lego website. Selenium can open up a chrome window and operate the browser using python commands. BeautifulSoup can take a string of html code and recognize the tags in it. It gives commands for calling tags and then performing methods with those tags (the tags are a class) - such as finding parents, siblings, and children that respect certain conditions.

- As a child I quite enjoyed lego, but I'm blown away by the surge in price for lego sets since purchasing them as a preteen. I'm quite intrigued to harvest data, particularly pricing data, and see if I can find trends.

## Milestone 3

- For this milestone, I ran into some hiccups. Selenium offers several means to find elements on a page - xpath, class, id and a couple others. However, I found these means to be quite limited. The only attribute that all elements share uniquely on lego's site is the xpath. And I had a couple unsettling experiences where it changed slightly and broke my code.

- Thus, I first resolved to find all elements through BeautifulSoup. BeautifulSoup's .find method offers a far more versatile means of calling elements. For example, one can pass a true / false function into the argument, and the method will run the function on each tag and return the first tag for which the function returns "true". This allows for much more reliable conditions in searching for elements. I wrote a method which generates the xpath for an element found through BeautifulSoup, allowing it to be fed into Selenium:

```
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
```

- The other key decision I made was compiling all elements I wish to interact with into a dictionary. The dictionary maps each element (given a descriptive name) to the condition used to call the element via BeautifulSoup's .find method and the parent element object through which .find will be called. I found centralizing and standardizing all the element interactions to be greatly beneficial in case one condition stops working and for keeping ugly addresses and conditions out of the flow of the code.

- Below is a part of the dictionary of relevant elements, and below that is the method which takes elements from the dictionary and yields the BeautifulSoup element object:

```
dictionary = {
    #Front page elements
    'age_check_overlay' : {
        'condition' : lambda tag : tag.has_attr('class') and tag['class'] == ['AgeGatestyles__Wrapper-xudtvj-0', 'itkEkg'],
        'dependency' : 'front_page'
    },
    
    'age_check_button' : {
        'condition' : lambda tag : tag.name == 'button' and tag.get_text() == 'Continue',
        'dependency' : 'age_check_overlay'
    },
    
    'cookie_accept_button' : {
        'condition' : lambda tag : tag.name == 'button' and tag.get_text() == 'Accept All',
        'dependency' : 'front_page'
    },
    
    #Product list elements
    'sets_checkbox_and_label' : {
        'condition' : lambda tag : tag.has_attr('data-test') and tag['data-test'] == 'checkbox-label' and \
            tag.find_all(lambda child : child.get_text().count('Sets') == 1) != [],
        'dependency' : 'product_list'
    },
    
    'sets_checkbox' : {
        'condition' : lambda tag : tag.has_attr('class') and tag['class'] == ['Checkboxstyles__CheckboxContainer-sc-19qo4tm-4', 'jrFByh'],
        'dependency' : 'sets_checkbox_and_label'
    },
    
    'page_info' : {
        'condition' : lambda tag : tag.has_attr('class') and tag['class'] == ['ProductGridstyles__Grid-lc2zkx-0', 'eGsxII'],
        'dependency' : 'product_list'
    },
    
    'show_all_button' : {
        'condition' : lambda tag : tag.has_attr('class') and tag['class'] == ['LinksNextstyles__AnchorButton-sc-1sxojvh-1', 'kARNPN', 'Paginationstyles__ShowAllLink-npbsev-13', 'iWkTte'],
        'dependency' : 'product_list'
    },
```

```
    def find_element_soup(self, element_name):
        
        element = self.elements[element_name]
        
        if element['dependency'] == self.webpage:
            parent = BeautifulSoup(self.driver.execute_script("return document.documentElement.outerHTML;"), 'html.parser')
        else:
            parent = self.find_element_soup(element['dependency'])
        
        return parent.find(element['condition'])
```

- In the dictionary, we see elements whose calling is greatly expedited by BeautifulSoup's functionality - The 'sets_checkbox_and_label' element is one of many checkboxes on the product list page - all with identical class names/structure. The only way to distinguish between them to my knowledge would be to use their position or to use the text in the label of its descendant (in this case, 'sets').

![picture](pictures/element_demo.png)

- The dictionary is long, but it makes the other methods and their calling very routine:

```
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
```

- I am proud of the readability of these methods. They choose elements via readable names:

```
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
```
