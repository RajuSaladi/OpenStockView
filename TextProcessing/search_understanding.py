def get_stock_info(input_string):
    stock_info_list = input_string.split(' ')
    stock_name = stock_info_list[0].upper()
    if len(stock_info_list) > 1:
        type_string = stock_info_list[1]+"minute"
    else:
        type_string = 'day'
    return stock_name, type_string
