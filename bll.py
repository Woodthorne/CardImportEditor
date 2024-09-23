from pathlib import Path

from dal import CardInfo, DataAccess


class BusinessLogic:
    def __init__(self, dal: DataAccess) -> None:
        self._dal = dal

    def get_source_target_paths(self) -> tuple[Path, Path]:
        source_path = self._dal.source_path
        target_path = self._dal.target_path

        return source_path, target_path
    
    def get_cards(self) -> list[CardInfo]:
        return self._dal.loaded_cards
    
    def import_cards(self) -> None:
        self._dal.import_cards()
    
    def export_cards(self) -> None:
        self._dal.export_cards()