import random
import tkinter as tk
from tkinter import Label

from utils.key_press_util import DirectionKeyEnum

class WindowUtil():


    def __init__(self):
        self.window_width: int = 600
        self.window_height: int = 600
        self.movement_size: int = 20
        self.root = tk.Tk()
        self.last_pressed_key: DirectionKeyEnum = DirectionKeyEnum.RIGHT
        self.snake_char: str = '🐍'
        self.snake: list[tk.Label] = []
        self.fruit_char: str = '🍎'
        self.fruit: tk.Label | None = None
        self.stop_snake: bool = False
        self.score: tk.Label | None = None


    def setWindow(self):
        self.root.title('Py Snake')
        
        # get the screen dimension
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # find the centre point
        centre_x = int(self.screen_width / 2 - self.window_width / 2)
        centre_y = int(self.screen_height / 2 - self.window_height / 2)

        # set the position of the window to the centre of the screen
        self.root.geometry(f'{self.window_width}x{self.window_height}+{centre_x}+{centre_y}')
        self.root.resizable(False, False)


    def setScore(self, text: int = 1):
        self.score = Label(self.root, text=text)
        self.score.place(x=20, y=10)


    def setSnakeInitial(self):
        centre_x = int(self.window_width / 2)
        centre_y = int(self.window_height / 2)
        
        snake = Label(self.root, text=self.snake_char)
        snake.place(x=centre_x, y=centre_y)
        
        self.snake = [snake]


    def incrementScore(self):
        if self.score is not None:
            currentScore = self.score.cget("text")
            newScore = currentScore + 1
            
            self.score.destroy()
            
            self.setScore(newScore)


    def moveSnake(self):
        if self.stop_snake:
            return
        
        lastIdxSnake: tk.Label = self.snake[len(self.snake) - 1]
        snakeHeadX = int(self.snake[0].place_info()["x"])
        snakeHeadY = int(self.snake[0].place_info()["y"])
        
        # move snake forward
        if self.last_pressed_key is DirectionKeyEnum.LEFT:
            snakeHeadX = snakeHeadX - self.movement_size
            
        if self.last_pressed_key is DirectionKeyEnum.RIGHT:
            snakeHeadX = snakeHeadX + self.movement_size
        
        if self.last_pressed_key is DirectionKeyEnum.UP:
            snakeHeadY = snakeHeadY - self.movement_size
            
        if self.last_pressed_key is DirectionKeyEnum.DOWN:
            snakeHeadY = snakeHeadY + self.movement_size
            
        isOutOfBounds = self.isOutOfBounds(snakeHeadX, snakeHeadY)
        hasCollided = self.hasCollided(snakeHeadX, snakeHeadY, True)
        
        if isOutOfBounds == False and hasCollided == False:
            newSnakeHead = Label(self.root, text=self.snake_char)
            newSnakeHead.place(x=snakeHeadX, y=snakeHeadY)
            
            self.snake.insert(0, newSnakeHead)
            
            # eat fruit, set new fruit
            if self.fruit is not None:
                fruitX = int(self.fruit.place_info()["x"])
                fruitY = int(self.fruit.place_info()["y"])
                
                if snakeHeadX == fruitX and snakeHeadY == fruitY:
                    self.incrementScore()
                    self.setFruit()
                
                # trim snake end
                else:
                    # remove snake char from screen
                    lastIdxSnake.destroy()
                    # remove from snake list
                    self.snake.pop()

 

    def setSnakeDirection(self, direction: DirectionKeyEnum):
        self.last_pressed_key = direction
        
    def setFruit(self):
        fruit_x = random.randrange(1, self.window_width)
        fruit_y = random.randrange(1, self.window_height)
        
        fruit_x = (round(fruit_x/self.movement_size)*self.movement_size)
        fruit_y = round(fruit_y/self.movement_size)*self.movement_size
        
        if fruit_x == self.window_width:
            fruit_x = fruit_x - self.movement_size
            
        if fruit_y == self.window_height:
            fruit_y = fruit_y - self.movement_size
            
        # generate another fruit if fruit placed on snake
        fruitSetOnSnake = self.hasCollided(fruit_x, fruit_y)
        if (fruitSetOnSnake == True):
            self.setFruit()
            return
        
        if self.fruit is None:
            self.fruit = Label(self.root, text=self.fruit_char)
        
        self.fruit.place(x=fruit_x, y=fruit_y)


    def isOutOfBounds(self, snakeHeadX: int, snakeHeadY: int) -> bool:
        if (snakeHeadX >= self.window_width or snakeHeadX < 0
            or snakeHeadY >= self.window_height or snakeHeadY < 0):
            self.endGame()            
            return True
        
        return False


    def hasCollided(self, x: int, y: int, endGame: bool = False) -> bool:
        hasCollided = False
        
        for pos in self.snake:
            posX = int(pos.place_info()["x"])
            posY = int(pos.place_info()["y"])
            
            if (posX == x and posY == y):
                hasCollided = True
                
                if endGame == True:
                    self.endGame()
                
        return hasCollided


    def endGame(self):
        self.stop_snake = True
        
        message = "GAME OVER"
        messageLen = len(message)
        centre_x = int(self.window_width / 2) - (messageLen * 3)
        centre_y = int(self.window_height / 2)
        
        self.gameOverMessage = Label(self.root, text=message)
        self.gameOverMessage.place(x=centre_x, y=centre_y)

        self.reset_button = tk.Button(self.root, text ="Play again?", command = self.resetGame)
        self.reset_button.pack(ipadx=10, ipady=10)


    def resetGame(self):
        # remove reset button and game over message
        self.reset_button.destroy()
        self.gameOverMessage.destroy()
        
        if self.score is not None:
            self.score.destroy()
        
        # remove old snake
        for pos in self.snake:
            pos.destroy()
        
        self.snake = []
        self.last_pressed_key = DirectionKeyEnum.RIGHT
        self.stop_snake = False
        
        self.setScore()
        self.setFruit()
        self.setSnakeInitial()