from utils import window_util
from utils.key_press_util import decodeKeyPress


window = window_util.WindowUtil()

root = window.setWindow()

def keyPressed(e: object):
    key = decodeKeyPress(e)
    
    if key is not None:
       window.setSnakeDirection(key)


window.root.bind("<Key>", keyPressed) 

window.setScore()
window.setFruit()
window.setSnakeInitial()

movement_ms = 150

def moveSnake():
    window.moveSnake()
    window.root.after(movement_ms, moveSnake)

# keep the window displaying
window.root.after(movement_ms, moveSnake)
window.root.mainloop()
