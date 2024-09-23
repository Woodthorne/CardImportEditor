import csv
from pathlib import Path


class CardInfo:
    def __init__(
            self,
            name: str = None,
            set_code: str = None,
            set_name: str = None,
            collector_number: int = None,
            foil: str = None,
            rarity: str = None,
            quantity: str = None,
            mana_box_id: int = None,
            scryfall_id: str = None,
            purchase_price: float = None,
            misprint: bool = None,
            altered: bool = None,
            condition: bool = None,
            language: str = None,
            purchase_price_currency: str = None
    ) -> None:
        self.name: str = name
        self.set_code: str = set_code
        self.set_name: str = set_name
        self.collector_number: int = collector_number
        self.foil: str = foil
        self.rarity: str = rarity
        self.quantity: int = quantity
        self.mana_box_id: int = mana_box_id
        self.scryfall_id: str = scryfall_id
        self.purchase_price: float = purchase_price
        self.misprint: bool = misprint
        self.altered: bool = altered
        self.condition: str = condition
        self.language: str = language
        self.purchase_price_currency: str = purchase_price_currency


class DataAccess:
    def __init__(self) -> None:
        self._source_path = Path('source.csv')
        self._target_path = Path('target.csv')
        self._loaded_cards: list[CardInfo] = []

    @property
    def source_path(self) -> Path:
        return self._source_path
    
    @property
    def target_path(self) -> Path:
        return self._target_path
    
    @property
    def loaded_cards(self) -> list[CardInfo]:
        return self._loaded_cards

    def import_cards(self) -> None:
        self._loaded_cards = []
        with open(self.source_path, 'r', encoding = 'utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                card = CardInfo(
                    name = row['Name'],
                    set_code = row['Set code'],
                    set_name = row['Set name'],
                    collector_number = row['Collector number'],
                    foil = row['Foil'],
                    rarity = row['Rarity'],
                    quantity = row['Quantity'],
                    mana_box_id = row['ManaBox ID'],
                    scryfall_id = row['Scryfall ID'],
                    purchase_price = row['Purchase price'],
                    misprint = ['Misprint'],
                    altered = ['Altered'],
                    condition = ['Condition'],
                    language = ['Language'],
                    purchase_price_currency = ['Purchase price currency']
                )
                self._loaded_cards.append(card)
    
    def export_cards(self) -> None:
        if len(self._loaded_cards) < 1:
            return
        
        fieldnames = [
            'Name',
            'Set code',
            'Set name',
            'Collector number',
            'Foil',
            'Rarity',
            'Quantity',
            'ManaBox ID',
            'Scryfall ID',
            'Purchase price',
            'Misprint',
            'Altered',
            'Condition',
            'Language',
            'Purchase price currency'
        ]
        
        with open(self.target_path, 'w', encoding = 'utf-8', newline = '') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
            writer.writeheader()
            for card in self._loaded_cards:
                card_dict = {
                    'Name': card.name,
                    'Set code': card.set_code,
                    'Set name': card.set_name,
                    'Collector number': card.collector_number,
                    'Foil': card.foil,
                    'Rarity': card.rarity,
                    'Quantity': card.quantity,
                    'ManaBox ID': card.mana_box_id,
                    'Scryfall ID': card.scryfall_id,
                    'Purchase price': card.purchase_price,
                    'Misprint': card.misprint,
                    'Altered': card.altered,
                    'Condition': card.condition,
                    'Language': card.language,
                    'Purchase price currency': card.purchase_price_currency
                }
                writer.writerow(card_dict)
    