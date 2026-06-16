# 1) ~~Сделать очищение grid перед новой вставкой unit'а в grid~~
# 2) ~~Сделать проверку на столкновение unit'а со стенками. И затем оставлять его в тех же координатах~~
# 3) ~~Сделать задержку отрисовки unit'а~~
# 4) ~~Сделать перемещение unit'а вниз с задержкой в 0.1 секунды (каждые 6 FPS)~~
# 5) ~~Сделать функции move_down, move_left и move_right в unit~~
# 6) ~~Сделать перемещение по горизонтали с проверками~~
# 7) ~~Сделать запекание unit'а при достижении нижней стенки~~
# 8) ~~Сделать генерацию нового unit'а после запекания~~
# 9) ~~Добавить картинки в unit~~
# 10) ~~Сделать так чтобы в запечённых клетках оставались картинки юнита~~
# 11) Внешний вид
# -- 1) ~~Типы юнитов~~
# -- 2) ~~2 цвета~~
# -- 3) ~~Имена~~
# -- 4) ~~Фигуры~~
# -- 5) ~~Картинки~~
# -- 6) ~~Генерация типа юнита~~
# -- 7) ~~Генерация цвета, на основе типа~~
# -- 8) ~~Генерация имени, на основе типа~~
# -- 9) ~~Генерация фигуры~~
# -- 10) ~~Генерация картинки, на основе типа~~
# -- 11) ~~Исправить ошибки перемещения~~
# -- 12) ~~Сделать переворот фигуры~~
# 12) Урон
# -- 1) ~~Хорошие наносят урон плохим и на оборот~~
# 13) Способности
# -- 1) Написать блок способностей

from icecream import ic
import pygame as pg

from pygame.image import load
from pygame.transform import scale_by

from classes.class_Cell import Cell
from classes.class_Unit import Unit

from pygame.locals import QUIT, K_ESCAPE, KEYDOWN, RESIZABLE, FULLSCREEN, K_UP, K_LEFT, K_RIGHT, K_DOWN
from pygame.key import get_pressed

class Battlefield:
    def __init__(self, screen):
        self.scr = screen
        self.scr_width = self.scr.get_width()
        self.scr_height = self.scr.get_height()
        self.bg = (255, 255, 255)
        
        self.bg = load('./images/Battlefield.png').convert_alpha()
        self.bg = pg.transform.smoothscale(self.bg, (self.scr_width, self.scr_height))
        
        self.cell_size = 128
        self.rows = 8
        self.cols = 8

        self.field_width = self.cell_size * self.cols + ((self.cols - 1) * 5)
        self.field_height = self.cell_size * self.rows + ((self.rows - 1) * 5)

        self.field_x = (self.scr_width - self.field_width) // 2
        self.field_y = (self.scr_height - self.field_height)
        
        self.empty_cell = Cell()
        
        self.grid = [
            [Cell() for _ in range(self.cols)] for _ in range(self.rows)
        ]
        
        self.unit = Unit(
            self.place_unit_in_grid,
            self.grid,
            self.cell_size,
            self.can_move_down,
            self.can_move_left,
            self.can_move_right
        )        
        
        self.frame_counter = 0
        self.move_delay = 30
        self.press_delay = 3
    
    def move(self):
        self.frame_counter += 1

        if self.frame_counter % self.move_delay == 0:
            self.unit.move()

        keys = get_pressed()
        
        if self.frame_counter % self.press_delay == 0:
            if keys[K_DOWN]:
                self.unit.move_down()
            if keys[K_LEFT]:
                self.unit.move_left()
            if keys[K_RIGHT]:
                self.unit.move_right()
            if keys[K_UP]:
                self.unit.rotate()

    def draw(self):
        for row in range(self.rows):
            for col in range(self.cols):                
                x = self.field_x + col * self.cell_size + (col * 5)
                y = self.field_y + row * self.cell_size + (row * 5)
                
                # self.scr.blit(self.grid[row][col].image, (x, y))
                
                # pg.draw.rect(
                #     self.scr,
                #     self.grid[row][col].bg_color,
                #     (
                #         x, y,
                #         self.cell_size, self.cell_size
                #     )
                # )
                
                if self.grid[row][col].type == 'cell':
                    pg.draw.rect(
                        self.scr,
                        self.grid[row][col].bg_color,
                        (
                            x, y,
                            self.cell_size, self.cell_size
                        )
                    )
                
                if self.grid[row][col].type == 'unit' or self.grid[row][col].type == 'baked':
                    pg.draw.rect(
                        self.scr,
                        self.grid[row][col].bg_color,
                        (
                            x, y,
                            self.cell_size, self.cell_size
                        )
                    )
                    
                    self.scr.blit(self.grid[row][col].image, (x, y))
    
    def clear_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col].type == 'unit':
                    self.grid[row][col] = Cell()

    def can_move_down(self, figure, grid_row, grid_col):
        for unit_row, row in enumerate(figure):
            for unit_col, cell in enumerate(row):
                if cell.type == 'unit':
                    next_row = grid_row + unit_row
                    next_col = grid_col + unit_col

                    if next_row >= len(self.grid):
                        self.baking_cells()
                        
                        is_wall_bottom = False
                        is_move_down = True
                        
                        return is_wall_bottom, is_move_down
                        
                    current_cell = self.grid[grid_row + unit_row - 1][grid_col + unit_col]
                    next_cell = self.grid[next_row][next_col]

                    # if next_cell.type != 'cell' and next_cell.type != 'unit':
                    if next_cell.type == 'baked':
                        if next_cell.unit_type != current_cell.unit_type:
                            ic('#' * 100)
                            ic(next_cell.unit_type)
                            ic(current_cell.unit_type)
                            
                            next_cell = Cell()
                            continue
                    
                        self.baking_cells()
                        
                        is_wall_bottom = False
                        is_move_down = True
                        
                        return is_wall_bottom, is_move_down

        is_wall_bottom = False
        is_move_down = True
        return is_wall_bottom, is_move_down

    def can_move_left(self, figure, grid_row, grid_col):
        for unit_row, row in enumerate(figure):
            for unit_col, cell in enumerate(row):
                if cell.type == 'unit':
                    # left_col = grid_col - unit_col
                    left_col = grid_col

                    if left_col < 0:
                        return False

                    next_cell = self.grid[grid_row][left_col]

                    if next_cell.type != 'cell' and next_cell.type != 'unit':
                        return False
        
        return True

    def can_move_right(self, figure, grid_row, grid_col):
        for unit_row, row in enumerate(figure):
            for unit_col, cell in enumerate(row):
                if cell.type == 'unit':
                    right_col = grid_col + unit_col
                    # right_col = grid_col
                    ic(f"Проверяем grid_col: {right_col}")

                    if right_col >= len(self.grid[0]):
                        return False

                    next_cell = self.grid[grid_row][right_col]

                    if next_cell.type != 'cell' and next_cell.type != 'unit':
                        return False
        
        return True
                    
    
    def place_unit_in_grid(
        self,
        figure,
        grid_row=0,
        grid_col=0
    ):        
        self.clear_grid()
        
        for unit_row, row in enumerate(figure):
            for unit_col, cell in enumerate(row):
                if cell.type == 'unit':
                    self.grid[grid_row + unit_row][grid_col + unit_col] = cell

    def baking_cells(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col].type != 'unit':
                    continue
                
                # ic(vars(self.grid[row][col]))
                
                self.grid[row][col] = Cell(
                    'baked',
                    (0, 255, 0),
                    self.grid[row][col].image,
                    self.grid[row][col].unit_type,
                    self.grid[row][col].unit_name
                )
        
        self.unit.generate()