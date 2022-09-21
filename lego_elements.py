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
        'condition' : lambda tag : tag.has_attr('class') and tag['class'] == ['ProductGridstyles__Grid-lc2zkx-0' 'eGsxII'],
        'dependency' : 'product_list'
    },
    
    'show_all_button' : {
        'condition' : lambda tag : tag.has_attr('class') and tag['class'] == ['LinksNextstyles__AnchorButton-sc-1sxojvh-1', 'kARNPN', 'Paginationstyles__ShowAllLink-npbsev-13', 'iWkTte'],
        'dependency' : 'product_list'
    },
    
    'page_bottom_post_show_all' : {
        'condition' : lambda tag : tag.has_attr('class') and tag['class'] == ['Scrollstyles__Container-sc-1370r7z-0', 'kvnbhA'],
        'dependency' : 'product_list'
    },
    
    'showing_x_of_y_text' : {
        'condition' : lambda tag : tag.name == 'div',
        'dependency' : 'page_bottom_post_show_all'
    },
    
    'survey_window' : {
        'condition' : lambda tag : tag.has_attr('id') and tag['id'] == 'IPEdContainer',
        'dependency' : 'product_list'
    },
    
    'survey_window_no' : {
        'condition' : lambda tag : tag.has_attr('id') and tag['id'] == 'noButton',
        'dependency' : 'survey_window'
    }
    
    #Details page elements
}


# 'page_info_and_bottom' : {
#     'condition' : lambda tag : tag.has_attr('class') and tag['class'] == ['ProductListingsstyles__ProductsWrapper-sc-1taio5c-2' 'dFBaNn'],
#     'dependency' : 'product_list'
# }

# 'page_bottom_pre_show_all' : {
#     'condition' : lambda tag : tag.has_attr('class') and tag['class'] == ['Paginationstyles__Container-npbsev-0', 'jxPRsL'],
#     'dependency' : 'page_info_and_bottom'
# }

# 'page_bottom_post_show_all' : {
#     'condition' : lambda tag : tag.has_attr('class') and tag['class'] == ['Scrollstyles__Container-sc-1370r7z-0', 'kvnbhA'],
#     'dependency' : 'page_info_and_bottom'
# }