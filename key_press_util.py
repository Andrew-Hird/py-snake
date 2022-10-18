from enum import Enum

class DirectionKeyEnum(str, Enum):
    UP = "Up"
    DOWN = "Down"
    LEFT = "Left"
    RIGHT = "Right"

def decodeKeyPress(e: object) -> DirectionKeyEnum | None:
    key: str = e.keysym
    
    try:
        return DirectionKeyEnum(key)
    except:
        return None
    
     