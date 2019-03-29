#!/usr/bin/python3

import pygame
import datetime as dt
import random
import os


class MineBoard(object):
    def __init__(self):
        self.mine = 0
        self.state = "unopened"
        self.number = 0
        self.checked = 0


class MineSweeper(object):
    def __init__(self, level='Expert'):
        self.levelSelect(level)
        self.loadImage()
        self.loaddict()
        self.display = pygame.display.set_mode(self.DISPLAY_SIZE)
        pygame.display.set_caption("지뢰찾기")
        self.init()

    def init(self):
        self.Boards = [[MineBoard() for a in range(self.LENGTH)] for b in range(self.HEIGHT)]
        self.TIME = None
        self.failed = 0
        self.win = 0
        self.number_of_mine = None
        self.opening_board = None
        self.opening_boards = None
        self.display.blit(self.newgame, (0, 0))

    def levelSelect(self, level):
        if level == 'Expert':
            self.HEIGHT = 16
            self.LENGTH = 30
            self.NUM_OF_MINE = 99
            self.DISPLAY_SIZE = (498, 316)
            print('Level: Expert')

    def loadImage(self):
        RELATIVE_ADDRESS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images', '')
        self.newgame = pygame.image.load(RELATIVE_ADDRESS + "newgame.png")
        self.game_new = pygame.image.load(RELATIVE_ADDRESS + "game_new.png")
        self.game_failed = pygame.image.load(RELATIVE_ADDRESS + "game_failed.png")
        self.game_reset = pygame.image.load(RELATIVE_ADDRESS + "game_reset.png")
        self.game_win = pygame.image.load(RELATIVE_ADDRESS + "game_win.png")
        self.unopened = pygame.image.load(RELATIVE_ADDRESS + "unopened.png")
        self.opening = pygame.image.load(RELATIVE_ADDRESS + "opening.png")
        self.mine_detected = pygame.image.load(RELATIVE_ADDRESS + "mine_detected.png")
        self.mine_exploded = pygame.image.load(RELATIVE_ADDRESS + "mine_exploded.png")
        self.mine_unexploded = pygame.image.load(RELATIVE_ADDRESS + "mine_unexploded.png")
        self.mine_wrong = pygame.image.load(RELATIVE_ADDRESS + "mine_wrong.png")
        self.mine_0 = pygame.image.load(RELATIVE_ADDRESS + "mine_0.png")
        self.mine_1 = pygame.image.load(RELATIVE_ADDRESS + "mine_1.png")
        self.mine_2 = pygame.image.load(RELATIVE_ADDRESS + "mine_2.png")
        self.mine_3 = pygame.image.load(RELATIVE_ADDRESS + "mine_3.png")
        self.mine_4 = pygame.image.load(RELATIVE_ADDRESS + "mine_4.png")
        self.mine_5 = pygame.image.load(RELATIVE_ADDRESS + "mine_5.png")
        self.mine_6 = pygame.image.load(RELATIVE_ADDRESS + "mine_6.png")
        self.mine_7 = pygame.image.load(RELATIVE_ADDRESS + "mine_7.png")
        self.time_0 = pygame.image.load(RELATIVE_ADDRESS + "time_0.png")
        self.time_1 = pygame.image.load(RELATIVE_ADDRESS + "time_1.png")
        self.time_2 = pygame.image.load(RELATIVE_ADDRESS + "time_2.png")
        self.time_3 = pygame.image.load(RELATIVE_ADDRESS + "time_3.png")
        self.time_4 = pygame.image.load(RELATIVE_ADDRESS + "time_4.png")
        self.time_5 = pygame.image.load(RELATIVE_ADDRESS + "time_5.png")
        self.time_6 = pygame.image.load(RELATIVE_ADDRESS + "time_6.png")
        self.time_7 = pygame.image.load(RELATIVE_ADDRESS + "time_7.png")
        self.time_8 = pygame.image.load(RELATIVE_ADDRESS + "time_8.png")
        self.time_9 = pygame.image.load(RELATIVE_ADDRESS + "time_9.png")

    def loaddict(self):
        self.TIME_IMAGE = {
            '0': self.time_0,
            '1': self.time_1,
            '2': self.time_2,
            '3': self.time_3,
            '4': self.time_4,
            '5': self.time_5,
            '6': self.time_6,
            '7': self.time_7,
            '8': self.time_8,
            '9': self.time_9
        }
        self.MINE_IMAGE = {
            0: self.mine_0,
            1: self.mine_1,
            2: self.mine_2,
            3: self.mine_3,
            4: self.mine_4,
            5: self.mine_5,
            6: self.mine_6,
            7: self.mine_7
        }
        self.TIME_POS = {
            "mine h'_digit": (14, 12),
            "mine t'_digit": (27, 12),
            "mine u'_digit": (40, 12),
            "time h'_digit": (443, 12),
            "time t'_digit": (456, 12),
            "time u'_digit": (469, 12)
        }

    def preReset(self):
        self.display.blit(self.game_reset, (235, 11))

    def postReset(self):
        self.init()

    def newGame(self, x, y):
        print('newGame')

        self.Boards = [[MineBoard() for a in range(self.LENGTH)] for b in range(self.HEIGHT)]

        # sample mine data
        around_boards = self.around(x, y)
        sample = [0] * (self.HEIGHT * self.LENGTH - 1 - len(around_boards))
        for i in range(self.NUM_OF_MINE): sample[i] = 1
        random.shuffle(sample)

        # sample data to self.Board.mine
        for y_, row in enumerate(self.Boards):
            for x_, board in enumerate(row):
                if (x_, y_) in around_boards + [(x, y)]:
                    # board.mine = 0
                    continue
                else:
                    board.mine = sample.pop()

        # self.Board.number
        for y in range(self.HEIGHT):
            for x in range(self.LENGTH):
                rst = 0
                for (num1, num2) in self.around(x, y):
                    if self.Boards[num2][num1].mine:
                        rst += 1
                self.Boards[y][x].number = rst

        # print mine data map
        for k in range(self.LENGTH):
            if k == 0: print(end=' ' * 2)
            print(str(k).rjust(3), end='')
            if k == self.LENGTH - 1: print()
        for k, row in enumerate(self.Boards): print(str(k).ljust(2), [board.mine for board in row])
        print()

        return self.Boards

    def searchMine(self, x, y, FIRST_TIME=0):
        if not self.Boards:
            print('No game.')
        if FIRST_TIME:
            self.newGame(x, y)
            self.searchMine(x, y)

        if self.Boards[y][x].checked == 0:
            if self.Boards[y][x].mine:
                self.display.blit(self.game_failed, (235, 11))
                self.display.blit(self.mine_exploded, (16 * x + 8, 16 * y + 50))
                self.failed = 1
                self.TIME = None
            elif self.Boards[y][x].number == 0 and self.Boards[y][x].state != 'opened':
                self.display.blit(self.MINE_IMAGE[self.Boards[y][x].number], (16 * x + 8, 16 * y + 50))
                self.Boards[y][x].state = 'opened'
                around_boards = self.around(x, y)
                for (num1, num2) in around_boards:
                    self.searchMine(num1, num2)
            else:
                self.display.blit(self.MINE_IMAGE[self.Boards[y][x].number], (16 * x + 8, 16 * y + 50))
                self.Boards[y][x].state = 'opened'

    def searchingMine(self, x, y):
        # print('method searchingMine')
        # print(self.Boards[y][x].state, self.Boards[y][x].checked)
        if self.Boards[y][x].state == 'unopened' and self.Boards[y][x].checked == 0:
            self.display.blit(self.opening, (16 * x + 8, 16 * y + 50))
            self.Boards[y][x].state = 'opening'
            self.opening_board = (x, y)

    def searchingBoard(self, x, y):
        around_boards = self.around(x, y) + [(x, y)]
        self.opening_boards = []
        for board in around_boards:
            x_, y_ = board[0], board[1]
            if self.Boards[y_][x_].state == 'unopened' and self.Boards[y_][x_].checked == 0:
                self.display.blit(self.opening, (16 * x_ + 8, 16 * y_ + 50))
                self.Boards[y_][x_].state = 'opening'
                self.opening_boards.append((x_, y_))

    def searchedBoard(self, x, y):
        around_boards = self.around(x, y)
        mines_checked = [self.Boards[y_][x_].checked for (x_, y_) in around_boards].count(1)
        mines_exist = [self.Boards[y_][x_].mine for (x_, y_) in around_boards].count(1)
        # print(mines_checked, mines_exist)

        if self.Boards[y][x].state == 'opened' and mines_exist == mines_checked:
            for board_pos in around_boards:
                x_, y_ = board_pos[0], board_pos[1]
                board = self.Boards[y_][x_]
                if board.state != 'opened':
                    if board.checked and not board.mine:
                        self.display.blit(self.mine_wrong, (16 * x_ + 8, 16 * y_ + 50))
                        board.state = 'opened'
                        self.failed = 1
                        self.TIME = None
                    elif not board.checked and board.mine:
                        self.display.blit(self.mine_exploded, (16 * x_ + 8, 16 * y_ + 50))
                        board.state = 'opened'
                        self.failed = 1
                        self.TIME = None
                    elif board.checked and board.mine:
                        pass
                    elif not board.checked and not board.mine:
                        self.searchMine(x_, y_)
                        board.state = 'opened'
        else:
            for board_pos in around_boards + [(x, y)]:
                x_, y_ = board_pos[0], board_pos[1]
                board = self.Boards[y_][x_]
                if board.state != 'opened' and not board.checked:
                    self.display.blit(self.unopened, (16 * x_ + 8, 16 * y_ + 50))
                    board.state = 'unopened'

    def checkMine(self, x, y):
        def mineShow(num_idx, pos_idx):
            self.display.blit(self.TIME_IMAGE[num_idx], self.TIME_POS[pos_idx])

        if self.number_of_mine is None:
            self.number_of_mine = self.NUM_OF_MINE

        if self.Boards[y][x].state == 'unopened':
            if self.Boards[y][x].checked == 0:
                self.display.blit(self.mine_detected, (16 * x + 8, 16 * y + 50))

                self.number_of_mine -= 1
                mine_str = str(self.number_of_mine).zfill(3)
                mineShow(mine_str[0], "mine h'_digit")
                mineShow(mine_str[1], "mine t'_digit")
                mineShow(mine_str[2], "mine u'_digit")

                self.Boards[y][x].checked = 1

            else:
                self.display.blit(self.unopened, (16 * x + 8, 16 * y + 50))

                self.number_of_mine += 1
                mine_str = str(self.number_of_mine).zfill(3)
                mineShow(mine_str[0], "mine h'_digit")
                mineShow(mine_str[1], "mine t'_digit")
                mineShow(mine_str[2], "mine u'_digit")

                self.Boards[y][x].checked = 0

    def dragging_left(self, x, y):
        x_, y_ = self.opening_board[0], self.opening_board[1]
        if self.Boards[y_][x_].state != 'opened':
            self.display.blit(self.unopened, (16 * x_ + 8, 16 * y_ + 50))
            self.Boards[y_][x_].state = 'unopened'
        self.searchingMine(x, y)

    def dragging_center(self, x, y):
        for x_, y_ in self.opening_boards:
            if self.Boards[y_][x_].state != 'opened':
                self.display.blit(self.unopened, (16 * x_ + 8, 16 * y_ + 50))
                self.Boards[y_][x_].state = 'unopened'
        self.searchingBoard(x, y)

    def timePassed(self):
        def timeShow(num_idx, pos_idx):
            self.display.blit(self.TIME_IMAGE[num_idx], self.TIME_POS[pos_idx])

        if self.TIME:
            CURRENT_TIME = dt.datetime.today()
            TIME_DELTA = CURRENT_TIME - self.TIME + dt.timedelta(0, 1)
            time_str = str(TIME_DELTA.seconds).zfill(3)
            timeShow(time_str[0], "time h'_digit")
            timeShow(time_str[1], "time t'_digit")
            timeShow(time_str[2], "time u'_digit")
            if time_str == '999':
                self.TIME = 0

    def forWin(self):
        count = 0
        for y_, row in enumerate(self.Boards):
            for x_, board in enumerate(row):
                if board.mine == 0 and board.state == 'opened':
                    count += 1
        if count == self.HEIGHT * self.LENGTH - self.NUM_OF_MINE:
            self.display.blit(self.game_win, (235, 11))
            self.win = 1
            self.TIME = None

    def game_exit(self):
        for y_, row in enumerate(self.Boards):
            for x_, board in enumerate(row):
                if board.mine and not board.checked and board.state == 'unopened':
                    if self.win:
                        self.display.blit(self.mine_detected, (16 * x_ + 8, 16 * y_ + 50))
                    else:
                        self.display.blit(self.mine_unexploded, (16 * x_ + 8, 16 * y_ + 50))

    def around(self, x, y):
        boards_around = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x + 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
        rst_around = []
        for i_around, (num1, num2) in enumerate(boards_around):
            if -1 < num1 < self.LENGTH and -1 < num2 < self.HEIGHT:
                rst_around.append((num1, num2))
        return rst_around


def main():
    pygame.init()
    clock = pygame.time.Clock()
    minesweeper = MineSweeper(level='Expert')

    LOOP_CONDITION = 1

    while LOOP_CONDITION:
        minesweeper.timePassed()
        minesweeper.forWin()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                LOOP_CONDITION = 0
                break

            if event.type == 5 and 234 < event.pos[0] < 261 and 10 < event.pos[1] < 37:
                minesweeper.preReset()

            if event.type == 6 and 234 < event.pos[0] < 261 and 10 < event.pos[1] < 37:
                minesweeper.postReset()

            if not minesweeper.failed and not minesweeper.win:

                if event.type in (4, 5, 6):
                    x = (event.pos[0] - 8) // 16
                    y = (event.pos[1] - 50) // 16

                    if -1 < x < minesweeper.LENGTH and -1 < y < minesweeper.HEIGHT:

                        if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
                            minesweeper.dragging_left(x, y)

                        if event.type == pygame.MOUSEMOTION and event.buttons[1] == 1:
                            minesweeper.dragging_center(x, y)

                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            minesweeper.searchingMine(x, y)

                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                            minesweeper.searchingBoard(x, y)

                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                            minesweeper.checkMine(x, y)

                        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                            if minesweeper.TIME is None:
                                minesweeper.TIME = dt.datetime.today()
                                minesweeper.searchMine(x, y, FIRST_TIME=1)
                            else:
                                minesweeper.searchMine(x, y)

                        if event.type == pygame.MOUSEBUTTONUP and event.button == 2:
                            minesweeper.searchedBoard(x, y)

            else:
                minesweeper.game_exit()

        pygame.display.update()

        clock.tick(100)

    pygame.quit()


if __name__ == '__main__':
    main()
