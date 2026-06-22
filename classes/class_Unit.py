import pygame as pg
from icecream import ic

from random import choice
from pygame.image import load

from config import types, colors, names, figures, icons, hp

from classes.class_Cell import Cell

class Unit:
    def __init__(
        self,
        place_unit_in_grid,
        grid,
        cell_size,
        can_move_down,
        can_move_left,
        can_move_right,
    ):
        self.type = 'unit'
        self.unit_id = 0

        self.place_unit_in_grid = place_unit_in_grid
        self.can_move_down = can_move_down
        self.can_move_left = can_move_left
        self.can_move_right = can_move_right

        self.grid = grid
        self.cell_size = cell_size
        
        self.generate()
    
    def generate(self):
        """
        Генерирует новый юнит.
        Возвращает True если юнит успешно заспавнился, False если нет места.
        """
        self.unit_id += 1
        
        self.unit_type = choice(types)
        self.bg_color = colors[self.unit_type]
        self.unit_name = choice(names[self.unit_type])
        self.unit_hp = hp[self.unit_name]
        self.layout_figure = figures[choice(list(figures.keys()))]
        ic(self.layout_figure)
        
        self.icon = icons[self.unit_name]
        self.icon_path = f'images/{self.icon}'
        
        self.image = load(self.icon_path).convert_alpha()
        self.image = pg.transform.smoothscale(
            self.image, (self.cell_size, self.cell_size)
        )
        ic(self.image)
        
        self.figure = self.generate_figure()
        
        self.grid_row = 0
        self.grid_col = (len(self.grid[0]) - len(self.figure[0])) // 2
        
        # 👇 ИЗМЕНЕНО: проверяем, можно ли заспавниться
        if not self.can_spawn():
            return False
        
        self.place_unit_in_grid(self.figure, self.grid_row, self.grid_col)
        return True
    
    def can_spawn(self):
        """
        Проверяет, можно ли заспавнить юнит в текущей позиции.
        Возвращает True если все клетки фигуры находятся на пустых клетках.
        """
        for unit_row, row in enumerate(self.figure):
            for unit_col, cell in enumerate(row):
                if cell.type == 'unit':
                    check_row = self.grid_row + unit_row
                    check_col = self.grid_col + unit_col
                    
                    if check_row >= len(self.grid) or check_col >= len(self.grid[0]):
                        return False
                    
                    if self.grid[check_row][check_col].type != 'cell':
                        return False
        return True
    
    def generate_figure(self):
        figure = [
            [
                0 for _ in range(len(self.layout_figure[0]))
            ] for _ in range(len(self.layout_figure))
        ]
        
        for cell_row, row in enumerate(self.layout_figure):
            for cell_col, cell in enumerate(row):
                if cell == "0":
                    figure[cell_row][cell_col] = Cell()
                elif cell == "X":
                    figure[cell_row][cell_col] = Cell(
                        self.type,
                        self.bg_color,
                        self.image,
                        self.unit_type,
                        self.unit_name,
                        self.unit_hp,
                        self.unit_id
                    )
        
        return figure
    
    def move(self):
        self.move_down()

    def move_down(self):
        grid_row = self.grid_row + 1
        
        is_wall_bottom, is_move_down = self.can_move_down(self.figure, grid_row, self.grid_col)

        if not is_move_down:
            return
        
        self.grid_row += 1
        ic("move_down call place_unit_in_grid")
        self.place_unit_in_grid(self.figure, self.grid_row, self.grid_col)

    def move_left(self):
        grid_col = self.grid_col - 1
        
        if not self.can_move_left(self.figure, self.grid_row, grid_col):
            return
        
        self.grid_col -= 1
        ic("move_left call place_unit_in_grid")
        self.place_unit_in_grid(self.figure, self.grid_row, self.grid_col)

    def move_right(self):
        grid_col = self.grid_col + 1
        
        if not self.can_move_right(self.figure, self.grid_row, grid_col):
            return
        
        self.grid_col += 1
        ic("move_right call place_unit_in_grid")
        self.place_unit_in_grid(self.figure, self.grid_row, self.grid_col)
    
    def rotate(self):
        self.figure = [list(row) for row in zip(*self.figure[::-1])]