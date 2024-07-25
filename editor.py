import csv
from pathlib import Path

from CoolFunctions import new_screen, print_menu


class Paginator:
    def __init__(self, all_items: list, chunk_size: int = 9) -> None:
        self.all_items = all_items
        self.chunk_start = 0
        self.chunk_end = 0
        self.chunk_size = chunk_size
        self.current_chunk = 0
        self.next_chunk()

        self.total_chunks = int(len(self.all_items) / self.chunk_size)
        if len(self.all_items) % self.chunk_size != 0:
            self.total_chunks += 1
    
    def next_chunk(self):
        if not self.next_possible():
            return
        
        self.chunk_start = self.chunk_end
        if self.chunk_end + self.chunk_size > len(self.all_items):
            self.chunk_end = len(self.all_items)
        else:
            self.chunk_end += self.chunk_size
        self.current_chunk += 1

    def prev_chunk(self):
        if not self.prev_possible():
            return
        
        self.chunk_end = self.chunk_start
        if self.chunk_start - self.chunk_size < 0:
            self.chunk_start = 0
        else:
            self.chunk_start -= self.chunk_size
        self.current_chunk -= 1
    
    def show_chunk(self):
        return self.all_items[self.chunk_start:self.chunk_end]

    def overwrite_chunk_item(self, new_data, chunk_index: int):
        absolute_index = self.chunk_start + chunk_index
        if absolute_index > len(self.all_items):
            return False
        else:
            self.all_items[absolute_index] = new_data
            return True
    
    def next_possible(self):
        if len(self.all_items) <= self.chunk_end:
            return False
        else:
            return True
    
    def prev_possible(self):
        if self.chunk_start <= 0:
            return False
        else:
            return True


class EditionEditor:
    def __init__(self) -> None:
        self.menu_header = 'Edition Editor'
        self.data_source: Path = Path('source.csv')
        self.target_source: Path = Path('target.csv')
    
    def main_menu(self):
        menu_options = ['Set source file',
                        'Set target file',
                        'Edit data'
                        ]
        description = None
        while True:
            listing = [f'Current source: {self.data_source}',
                        f'Current target: {self.target_source}']
            new_screen()
            print_menu(header = self.menu_header,
                       description = description,
                       listing = listing,
                       options = menu_options,
                       escape = 'Quit'
                       )
            description = None
            opt = input('>>> ')
            if opt == '0':
                quit()
            elif opt == '1':
                self.set_source()
            elif opt == '2':
                self.set_target()
            elif opt == '3':
                self.edit_data()
            else:
                description = 'Invalid option'
                
    
    def set_source(self):
        description = None
        while True:
            viable_paths = self.get_local_filepaths()
            opt_num = 0
            opt_nums = []
            options = []
            for path in viable_paths:
                opt_num += 1
                opt_nums.append(str(opt_num))
                options.append(str(opt_num) + '. ' + str(path))
            options.append('0. Return to main menu')
            new_screen()
            print_menu(header = self.menu_header + ' - Set source file',
                       description = description,
                       listing = options)
            opt = input('>>> ')
            if opt == '0':
                return
            elif opt in opt_nums:
                self.data_source = viable_paths[opt_nums.index(opt)]
                print(self.data_source)
                return
            else:
                description = 'Invalid option'
    
    def set_target(self):
        listing = ['Write exact name of target file (example: target.csv)',
                   '0. Return to main menu']
        description = None
        while True:
            new_screen()
            print_menu(header = self.menu_header + ' - Set target file',
                       description = description,
                       listing = listing)
            opt = input('>>> ')
            existing_paths = self.get_local_filepaths()
            existing_filenames = [str(path) for path in existing_paths]
            if opt == '0':
                return
            elif opt in existing_filenames:
                while True:
                    confirm_opt = input(f'File {opt} already exists. Overwrite contents? (y/n)').lower()
                    if confirm_opt == 'y':
                        self.target_source = Path(opt)
                        return
                    elif confirm_opt == 'n':
                        break
                    else:
                        print('Invalid input.')
            else:
                split_opt = opt.split('.')
                if len(split_opt) != 2:
                    description = 'Invalid filename. Must have exactly one period'
                elif split_opt[1] != 'csv':
                    description = 'Invalid fileformat. Must be .csv'
                else:
                    self.target_source = Path(opt)
                    return
    
    def edit_data(self):
        card_data: list[dict] = []
        with open(self.data_source, 'r', encoding = 'utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                card_data.append(row)
        
        if len(card_data) == 0:
            return
        card_pages = Paginator(card_data)
        
        while True:
            opt_next = None
            opt_prev = None
            listing = []
            options = [f'{card['Name']} ({card['Set code']} / {card['Collector number']})' for card in card_pages.show_chunk()]
            opts = [str(index + 1) for index in range(len(options))]
            if card_pages.prev_possible():
                listing.append('P.revious page')
                opt_prev = 'p'
            if card_pages.next_possible():
                listing.append('N.ext page')
                opt_next = 'n'
            
            new_screen()
            print_menu(header = f'{self.menu_header} - Cards (pg. {card_pages.current_chunk}/{card_pages.total_chunks})',
                       listing = listing,
                       options = options,
                       escape = 'Save to target'
                       )
            opt = input('>>> ').lower()
            if opt == '0':
                with open(self.target_source, 'w', encoding = 'utf-8', newline = '') as f:
                    writer = csv.DictWriter(f, fieldnames = card_data[0].keys())
                    writer.writeheader()
                    for row in card_data:
                        writer.writerow(row)
                return
            elif opt == opt_prev:
                card_pages.prev_chunk()
            elif opt == opt_next:
                card_pages.next_chunk()
            elif opt in opts:
                card: dict = card_pages.show_chunk()[opts.index(opt)]
                new_edition = input(f'Input new set code and collector number for {card['Name']} (format:SETCODE Collector#): ')
                new_edition = new_edition.split(' ')
                if len(new_edition) == 2:
                    card['Set code'] = new_edition[0].upper()
                    card['Collector number'] = new_edition[1]
                    card_pages.overwrite_chunk_item(card, opts.index(opt))

    def get_local_filepaths(self) -> list[Path]:
        directory = Path()
        viable_paths = directory.glob('*.csv')
        paths = []
        for path in viable_paths:
            paths.append(path)
        return paths

keys = ['Name', 'Set code', 'Set name', 'Collector number', 'Foil', 'Rarity', 'Quantity', 'ManaBox ID', 'Scryfall ID', 'Purchase price', 'Misprint', 'Altered', 'Condition', 'Language', 'Purchase price currency']

if __name__ == '__main__':
    editor = EditionEditor()
    editor.main_menu()