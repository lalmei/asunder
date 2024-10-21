from pydantic import BaseModel


# Base Metric class with Pydantic
class Metric(BaseModel):
    def __init__(self, name: str):
        self.name: str = name

    def calculate(self, **kwargs):
        pass

    def update(self, **kwargs):
        pass

    def reset(self):
        pass
