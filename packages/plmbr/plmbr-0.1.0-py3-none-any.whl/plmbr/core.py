import abc
import pandas as pd
import typing as tp

class Pipe:
    def __init__(self, name: str):
        self.name = name

    @abc.abstractmethod
    def flow(self, data: pd.DataFrame) -> pd.DataFrame:
        ...

class PipeLine:
    def __init__(self, pipes: list[Pipe], name: str = ""):
        self.pipes = pipes 
        self.name = name

    def flow(self, data: pd.DataFrame) -> pd.DataFrame:
        result = data.copy()
        for pipe in self.pipes:
            try:
                result = pipe.flow(result)
            except Exception as e:
                raise RuntimeError(f"PipeLine failed on {pipe.name}: {e}") from e
        return result
    
    def build(self) -> tp.Callable:
        def pipeline(data: pd.DataFrame) -> pd.DataFrame:
            return self.flow(data)
        return pipeline

    def __repr__(self):
        return str(
            pd.Series(
                [pipe.name for pipe in self.pipes],
                name=self.name if self.name else "Unnamed",
            )
        )