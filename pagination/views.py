from django.core.paginator import Paginator, InvalidPage, EmptyPage

def pagination(request, documents, page_number, number_post=25, number_page=10) :
    page_number = int(page_number)
    if len(documents) == 0 :
        return {
            'docs' : None,
            'pages' : None,
            'current_page' : None,
            'prev_page' : False,
            'next_page' : False
            }
    lv1_pages = Paginator(documents, number_post)
    lv2_pages = Paginator(lv1_pages.page_range, number_page)
    div = (page_number-1)/number_page+1

    # div = (page_number / number_page)
    # mod = page_number % number_page
    # if mod > 0 : div += 1

    pages = lv2_pages.page(div).object_list
 
    lv2_length = len(lv2_pages.page_range)
    if div == lv2_length : next_page = None
    else : next_page = lv2_pages.page(div+1).object_list[0]

    if div > 1 : prev_page = lv2_pages.page(div-1).object_list[-1]
    else : prev_page = None

    last_page = lv1_pages.page_range[-1]

    return {
        'docs' : lv1_pages.page(page_number).object_list,
        'pages' : pages,
        'current_page' : page_number,
        'prev_page' : prev_page,
        'next_page' : next_page,
        'last_page' : last_page
    }
