import pandas as pd
from .core import Pipe

class ReplaceValues(Pipe):
    def __init__(self, column: str, old_value: str, new_value: str, name: str = "ReplaceValues"):
        super().__init__(name)
        self.column = column
        self.old_value = old_value
        self.new_value = new_value

    def flow(self, data: pd.DataFrame) -> pd.DataFrame:
        data[self.column] = data[self.column].replace(self.old_value, self.new_value)
        return data
    
class ConvertType(Pipe):
    def __init__(self, column: str, dtype: type, name: str = "ConvertType"):
        super().__init__(name)
        self.column = column
        self.dtype = dtype

    def flow(self, data: pd.DataFrame) -> pd.DataFrame:
        data[self.column] = data[self.column].astype(self.dtype)
        return data
    
class DropDuplicates(Pipe):
    def __init__(self, subset: list[str] = None, keep: str = 'first', name: str = "DropDuplicates"):
        super().__init__(name)
        self.subset = subset
        self.keep = keep

    def flow(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.drop_duplicates(subset=self.subset, keep=self.keep)
    
class SortValues(Pipe):
    def __init__(self, by: str, ascending: bool = True, name: str = "SortValues"):
        super().__init__(name)
        self.by = by
        self.ascending = ascending

    def flow(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.sort_values(by=self.by, ascending=self.ascending)
