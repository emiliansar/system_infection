from icecream import ic
import pygame as pg

from pygame.image import load
from pygame.transform import scale_by

from classes.class_Cell import Cell
from classes.class_Unit import Unit

from pygame.locals import QUIT, K_ESCAPE, KEYDOWN, RESIZABLE, FULLSCREEN, K_UP, K_LEFT, K_RIGHT, K_DOWN
from pygame.key import get_pressed

class Battlefield:
    def __init__(self, screen, sound_manager=None):
        self.scr = screen
        self.sound_manager = sound_manager
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
        
        self.mission_points = 0
        
        self.frame_counter = 0
        self.move_delay = 30
        self.press_delay = 3
        
        self.game_over = False
        self.defeat = False  # 👇 ДОБАВЛЕНО: флаг поражения
    
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
                
                current_cell = self.grid[row][col]
                
                if current_cell.type == 'cell':
                    pg.draw.rect(
                        self.scr,
                        current_cell.bg_color,
                        (
                            x, y,
                            self.cell_size, self.cell_size
                        )
                    )
                
                if current_cell.type == 'unit' or current_cell.type == 'baked':
                    pg.draw.rect(
                        self.scr,
                        current_cell.bg_color,
                        (
                            x, y,
                            self.cell_size, self.cell_size
                        )
                    )
                    
                    self.scr.blit(current_cell.image, (x, y))
    
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

                    if next_cell.type == 'baked':
                        if next_cell.unit_type != current_cell.unit_type:
                            # 👇 Звук при столкновении РАЗНЫХ типов
                            if hasattr(self, 'sound_manager'):
                                self.sound_manager.play_negative_connect()
                            
                            self.mission_points += self.get_size_by_id(next_cell.unit_id)
                            
                            self.delete_cell_by_id(next_cell.unit_id)
                            self.unit.generate()
                        
                            is_wall_bottom = False
                            is_move_down = True
                            
                            return is_wall_bottom, is_move_down
                            
                        
                        # 👇 Звук при столкновении ОДИНАКОВЫХ типов
                        if next_cell.unit_type == current_cell.unit_type:
                            if hasattr(self, 'sound_manager'):
                                self.sound_manager.play_positive_connect()
                        
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
                    ic(f"Проверяем grid_col: {right_col}")

                    if right_col >= len(self.grid[0]):
                        return False

                    next_cell = self.grid[grid_row][right_col]

                    if next_cell.type != 'cell' and next_cell.type != 'unit':
                        return False
        
        return True

    def delete_cell_by_id(self, id):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col].unit_id == id:
                    self.grid[row][col] = Cell()
    
    def get_size_by_id(self, id):
        size = 0
        
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col].unit_id == id:
                    size += 1
        
        return size

    def get_cell_at(self, pos):
        mx, my = pos
        if not (self.field_x <= mx <= self.field_x + self.field_width and
                self.field_y <= my <= self.field_y + self.field_height):
            return None, None

        col = (mx - self.field_x) // (self.cell_size + 5)
        row = (my - self.field_y) // (self.cell_size + 5)

        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return None, None

        cell_x = self.field_x + col * self.cell_size + col * 5
        cell_y = self.field_y + row * self.cell_size + row * 5
        if not (cell_x <= mx <= cell_x + self.cell_size and
                cell_y <= my <= cell_y + self.cell_size):
            return None, None

        return row, col

    def apply_ability(self, ability_key, row, col):
        if ability_key == 'delete_1':
            return self._delete_1(row, col)
        elif ability_key == 'delete_9':
            return self._delete_9(row, col)
        elif ability_key == 'reset':
            return self._reset()
        return False

    def _delete_1(self, row, col):
        cell = self.grid[row][col]
        if cell.type != 'baked':
            return False
        self.grid[row][col] = Cell()
        return True

    def _delete_9(self, row, col):
        deleted_any = False
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                r, c = row + dr, col + dc
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    if self.grid[r][c].type == 'baked':
                        self.grid[r][c] = Cell()
                        deleted_any = True
        return deleted_any

    def _reset(self):
        self.grid = [
            [Cell() for _ in range(self.cols)] for _ in range(self.rows)
        ]
        self.unit.generate()
        self.game_over = True
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
                
                self.grid[row][col] = Cell(
                    'baked',
                    self.grid[row][col].bg_color,
                    self.grid[row][col].image,
                    self.grid[row][col].unit_type,
                    self.grid[row][col].unit_name,
                    self.grid[row][col].unit_hp,
                    self.grid[row][col].unit_id
                )
        
        # 👇 ИЗМЕНЕНО: проверяем результат generate()
        if not self.unit.generate():
            self.defeat = True