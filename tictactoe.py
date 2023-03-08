# based on.
# https://www.geeksforgeeks.org/tic-tac-toe-gui-in-python-using-pygame/

# check out https://github.com/MyreMylar/pygame_gui

# importing the required libraries
import pygame as pg
import sys
import time


class TicTacToe:
    def reset_game(self):
        self.player = 'x'
        self.draw = False
        self.winner = None
        self.board = [[None]*3, [None]*3, [None]*3]
        self.gameover = False
        

class Wrapper:
    def __init__(self):
        # pygame window
        
        self.tictactoe = TicTacToe()
        
        self.init_window()
        
        # this is stuff about game rules.
        self.build_check_data()
        self.reset_game()
        
        # this is data.
        self.colors = {"white": (255, 255, 255),
                       "red": (255,0,0),
                       "black": (0, 0, 0)}
        self.load_images()
        
        # this actually touches pygame.
        
        # setting fps manually
        self.fps = 30
        # this is used to track time
        self.CLOCK = pg.time.Clock()
        
        # start the game.
        self.game_start_window()
        self.reset_visuals(self.player)
        pg.display.update()
        
    def init_window(self,width=400,height=400):
        # initializing the pygame window
        pg.init()
        
        self.quit=False
        self.width = width
        self.height = height

        self.screen = pg.display.set_mode(
            (self.width, self.height + 100), 0, 32)

        pg.display.set_caption("My Tic Tac Toe")
        
    def load_images(self):
        
        cover = pg.image.load("modified_cover.png")
        x_img = pg.image.load("X_modified.png")
        y_img = pg.image.load("o_modified.png")

        # resizing images
        cover = pg.transform.scale(
            cover, (self.width, self.height + 100))
        x_img = pg.transform.scale(x_img, (80, 80))
        o_img = pg.transform.scale(y_img, (80, 80))

        self.images = {"x": x_img,
                       "o": o_img,
                       "cover":cover}

    def build_check_data(self):
        diags = [[(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]]
        regular = []
        x = 0
        while x < 3:
            regular.append([(x, 0), (x, 1), (x, 2)])
            x += 1

        y = 0
        while y < 3:
            regular.append([(0, y), (1, y), (2, y)])
            y += 1

        self.game_over_check_cells = diags+regular
    
    def game_start_window(self):
        # displaying over the screen
        self.screen.blit(self.images["cover"], (0, 0))
        pg.display.update()
        time.sleep(0.5)
        
    def main(self):
        for event in pg.event.get():
            event_str = str(event)

            if "Quit" in event_str:
                self.quit = True

            elif "MouseButtonDown" in event_str:
                
                row, col = self.user_click()
                valid_move = self.move_valid(row, col)
                
                if valid_move:
                    self.draw_move(self.player, row, col)
                    self.board[row-1][col-1] = self.player
                    self.toggle_player_turn()
                    
                self.draw_status(self.player)
                
                r, line = self.check_win()
                if r!= None:
                    self.draw_win(line,self.player)
                    pg.display.update()
                    time.sleep(0.5)
                    self.reset_game()
                    self.reset_visuals(self.player)
        
        pg.display.update()
        self.CLOCK.tick(self.fps)
        
    def user_click(self):
        # pygame doesn't have objects, at least not here.
        
        # kinda bad, doesn't have the concept of "tiles".
        # might be useful to explain the difference between
        # "regular coding" and objects.

        # get coordinates of mouse click
        x, y = pg.mouse.get_pos()
        col = int((x/self.width).__floordiv__(1/3)) + 1
        row = int((y/self.height).__floordiv__(1/3)) + 1

        if row == 4:
            row = None
            # this is kinda stupid. but there is a display
            # area that shouldn't accept clicks.
            # normally this would be handled by a proper object.
            
        return row,col
        
    def draw_game_board(self):
        
        self.screen.fill(self.colors["white"])

        line_color = self.colors["black"]

        # drawing vertical lines
        x1 = (1/3) * self.width
        x2 = (2/3) * self.width
        y1 = 0
        y2 = self.height

        
        pg.draw.line(self.screen, line_color, (x1, y1), (x1, y2), 7)
        pg.draw.line(self.screen, line_color, (x2, y1), (x2, y2), 7)

        # drawing horizontal lines
        x1 = 0
        x2 = self.width
        y1 = (1/3) * self.height
        y2 = (2/3) * self.height
    
        pg.draw.line(self.screen, line_color, (x1, y1), (x2, y1), 7)
        pg.draw.line(self.screen, line_color, (x1, y2), (x2, y2), 7)
    
    def draw_status(self,player):

        if self.winner is None:
            message = player + "'s Turn"
        else:
            message = self.winner + " won !"
        if self.draw:
            message = "Game Draw !"

        # setting a font object
        font = pg.font.Font(None, 30)

        # setting the font properties like
        # color and width of the text
        text = font.render(message, 1,self.colors["white"])

        # copy the rendered message onto the board
        # creating a small block at the bottom of the main display
        self.screen.fill((0, 0, 0), (0, 400, 500, 100))
        text_rect = text.get_rect(center=(self.width / 2, 500-50))
        self.screen.blit(text, text_rect)
        
    def check(self,line):

        symbols = []

        for p in line:
            val = self.board[p[1]][p[0]]
            symbols.append(val)

        symbols = list(set(symbols))
        if len(symbols) == 1:
            if symbols[0] != None:
                return symbols[0]

    def check_win(self):

        # what's the condition?
        # either a row or a column contains symbols of the same type.
        # or a diagonal.

        for line in self.game_over_check_cells:
            r = self.check(line)
            if r != None:
                self.winner = r
                return r, line
        
        return None, None
    
    def move_valid(self,row,col):
        
        unoccupied = self.board[row-1][col-1] == None
        valid_move = (row and col and unoccupied )
        
        return valid_move
    
    def draw_win(self,line,player):
        p1 = line[0]
        p2 = line[-1]
        stepx = self.width/3
        stepy = self.height/3

        # e.g. (0+0.5) * 133px, (2+0.5) * 133px
        result_p1 = ((p1[0] + 0.5)*stepx, (p1[1] + 0.5)*stepy)
        result_p2 = ((p2[0] + 0.5)*stepx, (p2[1] + 0.5)*stepy)

        pg.draw.line(self.screen,
                     self.colors["red"],
                     result_p1,
                     result_p2,
                     4)

        if(all([all(row) for row in self.board]) and self.winner is None):
            draw = True
        
        self.draw_status(player)

    def draw_move(self, player, row, col):

        # calculate image position
        stepx = self.width / 3
        stepy = self.height / 3
        posx = (row-1) * stepx + 30
        posy = (col-1) * stepy + 30
        
        # update visuals
        self.screen.blit(self.images[player], (posy, posx))
        
    def toggle_player_turn(self):
        if(self.player == 'x'):
            self.player = 'o'
        else:
            self.player = 'x'
    
    def reset_game(self):
        self.player = 'x'
        self.draw = False
        self.winner = None
        self.board = [[None]*3, [None]*3, [None]*3]
        self.gameover = False
        
    def reset_visuals(self,player):
        self.draw_game_board()
        self.draw_status(player)
    
    def quit(self):
        self.quit=True
        pg.quit()

def main():
    Game = Wrapper()

    while True:
        Game.main()
        if Game.quit:
            break
            
if __name__ == "__main__":
    main()
    
