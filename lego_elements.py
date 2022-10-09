dictionary = {
    #Front page elements
    'age_check_overlay' : {
        'condition' : lambda tag : tag.has_attr('class') and tag['class'] == ['AgeGatestyles__Wrapper-xudtvj-0', 'itkEkg'],
        'dependency' : 'webpage'
    },
    
    'age_check_button' : {
        'condition' : lambda tag : tag.name == 'button' and tag.get_text() == 'Continue',
        'dependency' : 'age_check_overlay'
    },
    
    'cookie_accept_button' : {
        'condition' : lambda tag : tag.name == 'button' and tag.get_text() == 'Accept All',
        'dependency' : 'webpage'
    },
    
    #Product list elements
    'sets_checkbox_and_label' : {
        'condition' : lambda tag : tag.has_attr('data-test') and tag['data-test'] == 'checkbox-label' and \
            tag.find_all(lambda child : child.get_text().count('Sets') == 1) != [],
        'dependency' : 'webpage'
    },
    
    'sets_checkbox' : {
        'condition' : lambda tag : tag.has_attr('class') and tag['class'] == ['Checkboxstyles__CheckboxContainer-sc-19qo4tm-4', 'jrFByh'],
        'dependency' : 'sets_checkbox_and_label'
    },
    
    'page_info' : {
        'condition' : lambda tag : tag.has_attr('class') and tag['class'] == ['ProductGridstyles__Grid-lc2zkx-0', 'eGsxII'],
        'dependency' : 'webpage'
    },
    
    'show_all_button' : {
        'condition' : lambda tag : tag.has_attr('class') and tag['class'] == ['LinksNextstyles__AnchorButton-sc-1sxojvh-1', 'kARNPN', 'Paginationstyles__ShowAllLink-npbsev-13', 'iWkTte'],
        'dependency' : 'webpage'
    },
    
    'page_bottom_post_show_all' : {
        'condition' : lambda tag : tag.has_attr('class') and tag['class'] == ['Scrollstyles__Container-sc-1370r7z-0', 'kvnbhA'],
        'dependency' : 'webpage'
    },
    
    'showing_x_of_y_text' : {
        'condition' : lambda tag : tag.has_attr('class') and tag['class'] == ['Scrollstyles__ScrollInfo-sc-1370r7z-1', 'hOZxdU'],
        'dependency' : 'page_bottom_post_show_all'
    },
    
    'survey_window' : {
        'condition' : lambda tag : tag.has_attr('id') and tag['id'] == 'IPEdContainer',
        'dependency' : 'webpage'
    },
    
    'survey_window_no' : {
        'condition' : lambda tag : tag.has_attr('id') and tag['id'] == 'noButton',
        'dependency' : 'survey_window'
    },
    
    #Details page elements
    'item_description' : {
        'condition' : lambda tag : tag.has_attr('class') and tag['class'] == ['ProductDetailsPagestyles__ProductDynamicContentContainer-sc-1waehzg-6', 'iHKzHW'],
        'dependency' : 'webpage'
    },
    
    'item_stats' : {
        'condition' : lambda tag : tag.has_attr('class') and tag['class'] == ['ProductAttributesstyles__Container-sc-1sfk910-0', 'ctVkib'],
        'dependency' : 'webpage'
    },
    
    'item_rating' : {
        'condition' : lambda tag : tag.has_attr('class') and tag['class'] == ['ProductOverviewstyles__ProductBadgesRow-sc-1a1az6h-0', 'bCQoZx'],
        'dependency' : 'webpage'
    },
    
    'item_price' : {
        'condition' : lambda tag : tag.has_attr('class') and tag['class'] == ['ProductOverviewstyles__PriceAvailabilityWrapper-sc-1a1az6h-10', 'fCBTFc'],
        'dependency' : 'webpage'
    },
    
    'item_pictures' : {
        'condition' : lambda tag : tag.has_attr('class') and tag['class'] == ['MediaQuery__MediaHideable-sc-1poqfy2-0', 'fjfTGa', 'ProductMediaViewerstyles__MediaQueryThumbnailsHorizontal-sc-13pkbbe-2', 'gnVtlp'],
        'dependency' : 'webpage'
    }
}


front_page_link = 'https://www.lego.com/en-gb'
product_list_links = ['https://www.lego.com/en-au/categories/age-1-plus-years',
    'https://www.lego.com/en-au/categories/age-4-plus-years',
    'https://www.lego.com/en-au/categories/age-6-plus-years',
    'https://www.lego.com/en-au/categories/age-9-plus-years',
    'https://www.lego.com/en-au/categories/age-13-plus-years',
    'https://www.lego.com/en-au/categories/age-18-plus-years']


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

#'/html/body/div[1]/main'

#'/html/body/div[1]/main/div'

#description '/html/body/div[1]/main/div/div[2]/div/div/div'
#'ProductDetailsPagestyles__ProductDynamicContentContainer-sc-1waehzg-6', 'iHKzHW'

#stats: '/html/body/div[1]/main/div/div[1]/div/ div[1]/div[2]/div'
#'ProductAttributesstyles__Container-sc-1sfk910-0', 'ctVkib'

#rates: '/html/body/div[1]/main/div/div[1]/div/ div[2]/div[1]'
#'ProductOverviewstyles__ProductBadgesRow-sc-1a1az6h-0', 'bCQoZx'

#price: '/html/body/div[1]/main/div/div[1]/div/ div[2]/div[3]'
#'ProductOverviewstyles__PriceAvailabilityWrapper-sc-1a1az6h-10', 'fCBTFc'

#pictures: 'ThumbnailsTrackstyles__Track-sc-141n2vw-4', 'dHIUWk'