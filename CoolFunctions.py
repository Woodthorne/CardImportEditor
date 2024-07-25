def new_screen():
    '''
    Clears the screen, for windows and unix
    '''
    import os
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def print_menu(header: str,
               menu_width: int = 6,
               description: str = None,
               listing: list[str] = None,
               options: list[str] = None,
               escape: str = None
               ) -> None:
    '''
    Prints a bordered menu. Can contain description, lists, and options.
    
    header: Header of the menu.
    
    menu_width: Optional int. Specifies the minimum width of the menu.
        Defaults to 6 characters.

    description: Optional string. Wraps the string so that it fits within the
        width of the menu borders.
    
    listing: Optional list of strings. Produces unnumbered list.
    
    options: Optional list of option strings. Will get numbered starting
        at 1.
    
    escape: Optional string. Adds option "0." at the bottom of options.
        Useful for escaping option.
    
    
    '''
    if len(header) > 2:
        menu_width += len(header) - 2
    if listing:
        for item in listing:
            if len(item) + 4 > menu_width:
                menu_width = len(item) + 4
    if options:
        for item in options:
            if len(item) + 7 > menu_width:
                menu_width = len(item) + 7
    if escape and len(escape) + 7 > menu_width:
        menu_width = len(escape) + 7
    content_width = menu_width - 4

    print(f'=={header}{"=" * (content_width - len(header))}==')
    option_num = 0
    if description:
        if len(description) <= content_width:
            padding = content_width - len(description)
            print(f'| {description}{" " * padding} |')
        else:
            split_description = description.split(' ')
            while split_description:
                current_row = ''
                while split_description and len(current_row) \
                                            + len(split_description[0]) \
                                            + 1 \
                                                <= content_width:
                    current_row += ' ' + split_description.pop(0)
                padding = content_width - len(current_row)
                print(f'| {current_row}{" " * padding} |')
        print('=' * menu_width)
    
    if listing:
        for item in listing:
            padding = content_width - len(item)
            print(f'| {item}{" " * padding} |')
        print('=' * menu_width)

    if options:
        for item in options:
            option_num += 1
            padding = content_width - len(item) - 3
            print(f'| {option_num}. {item}{" " * padding} |')
    if escape:
        padding = content_width - len(escape) - 2
        print(f'| 0. {escape}{" " * padding}|')
    if options or escape:
        print('=' * menu_width)

def string_wrap(string: str, max_width: int) -> str:
    '''
    Rudimentary string wrapper which takes a string and maximum width and
    splits the rows at the blank space preceding a width-breaching word.
    '''
    if len(string) <= max_width:
        return string
    split_string = string.split(' ')
    new_string_list = []
    while split_string:
        current_row = []
        while split_string and len(current_row) \
                                + len(str(current_row)) \
                                + len(split_string[0]) \
                                <= max_width:
            current_row.append(split_string.pop(0))
        new_string_list.append(" ".join(current_row))
    new_string = '\n'.join(new_string_list)
    return new_string


if __name__ == '__main__':
    _693_words = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla sit amet volutpat massa. Phasellus malesuada massa id metus congue, sed imperdiet risus venenatis. Sed sollicitudin commodo sapien non condimentum. Donec iaculis accumsan lacus sed tincidunt. Aliquam volutpat tempus felis, sit amet pellentesque augue iaculis ut. Suspendisse ut risus viverra, elementum purus id, malesuada erat. Donec consequat malesuada orci, vel ultricies ex consequat eu. Curabitur et ultrices ex. Nulla faucibus luctus arcu a dignissim. Etiam eget dignissim est. Ut ut facilisis leo. Nunc ante tortor, luctus at mollis nec, porttitor in turpis. Maecenas ligula lacus, consectetur eu volutpat id, fermentum ut.'
    print_menu('Restaurant Menu',
               description = [_693_words, 40],
               escape = 'Finished',
               listing = ['Quick', 'Fast', 'Expedious'],
               options = ['Fish and Chips',
                          'Pasta Bolognese',
                          'A big bucket containing the leftovers from yesterday']
               )
#    print(roll_d(20,5))
#    print(string_wrap(_693_words, 79))
    print('Done')