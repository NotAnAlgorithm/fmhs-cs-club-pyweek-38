from . import dataclass, field, uuid4

@dataclass
class Rect:
    x:int
    y:int
    z:int
    w:int
    h:int

@dataclass
class Sprite:
    guid:str = field(default_factory = lambda: uuid4())
    rect:Rect = field(default_factory = lambda: None)
