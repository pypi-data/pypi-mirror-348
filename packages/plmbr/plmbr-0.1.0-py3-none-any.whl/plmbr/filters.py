import pandas as pd
from .core import Pipe 

class FilterWithFn(Pipe):
    def __init__(self, fn: callable, name: str = "FilterWithFn"):
        super().__init__(name)
        self.fn = fn

    def flow(self, data: pd.DataFrame) -> pd.DataFrame:
        return data[self.fn(data)]

class FilterByValue(Pipe):
    def __init__(self, column: str, value: str, name: str = "FilterByValue"):
        super().__init__(name)
        self.column = column
        self.value = value

    def flow(self, data: pd.DataFrame) -> pd.DataFrame:
        return data[data[self.column] == self.value]

class FilterColByType(Pipe):
    def __init__(self, dtype: type, name: str = "FilterByType"):
        super().__init__(name)
        self.dtype = dtype

    def flow(self, data: pd.DataFrame) -> pd.DataFrame:
        return data[data.apply(lambda x: isinstance(x, self.dtype), axis=1)]
    
class FilterNaN(Pipe):
    def __init__(self, name: str = "FilterNaN"):
        super().__init__(name)

    def flow(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.dropna()
    
class FilterNumericColumns(Pipe):
    def __init__(self, name: str = "FilterNumericColumns"):
        super().__init__(name)

    def flow(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.select_dtypes(include=[int, float])
    
class FilterCategoricalColumns(Pipe):
    def __init__(self, name: str = "FilterCategoricalColumns"):
        super().__init__(name)

    def flow(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.select_dtypes(include=['category', 'object'])
