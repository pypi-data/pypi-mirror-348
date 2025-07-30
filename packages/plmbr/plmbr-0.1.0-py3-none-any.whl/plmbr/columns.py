import pandas as pd
from .core import Pipe 

class DropColumns(Pipe):
    def __init__(self, columns: list[str], name: str = "DropColumns"):
        super().__init__(name)
        self.columns = columns

    def flow(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.drop(columns=self.columns) 

class RenameColumns(Pipe):
    def __init__(self, columns: dict[str, str], name: str = "RenameColumns"):
        super().__init__(name)
        self.columns = columns

    def flow(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.rename(columns=self.columns)
