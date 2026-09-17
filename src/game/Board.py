

from src.game.Cell import Cell, EmptyCell,  MineCell, NumberCell
import random


class Board:
    """ Board class representing the Minesweeper game board. """

    def __init__(self):
        #self.width = 30
        #self.height = 16
        #self.num_mines = 99
        self.width = 10
        self.height = 8
        self.num_mines = 3
        #self.grid: list[list[Cell]] = [[EmptyCell() for _ in range(30)] for _ in range(16)]
        self.grid: list[list[Cell]] = [[EmptyCell() for _ in range(self.width)] for _ in range(self.height)]
        self.initialized = False
        self.game_over = False
        self.game_won = True

    def initialize_game(self, x: int, y: int):
        """Initialize the game board. When first clicked, place mines and set up the board."""
        if self.initialized:
            return
        
        # Step 1: Get safe zone (first click + neighbors)
        safe_zone = self._get_safe_zone(x, y)
   
        # Step 2: Place mines randomly, avoiding safe zone
        self._place_mines(safe_zone)
        
        # Step 3: Calculate numbers for all non-mine cells
        self._calculate_numbers()

        self.initialized = True

    def number_of_mines(self) -> int:
        return self.num_mines

    def is_game_over(self) -> bool:
        return self.game_over

    def is_game_won(self) -> bool:
        """Check if the player has won by revealing all non-mine cells."""
        for y in range(self.height):
            for x in range(self.width):
                cell = self._get_cell(x, y)
                if not isinstance(cell, MineCell) and not cell.is_revealed():
                    return False
        return True

    def flag_cell(self, x: int, y: int):
        self._get_cell(x, y).flag()

    def click_cell(self, x: int, y: int):
        if not self.initialized:
            self.initialize_game(x, y)
        
        cell = self._get_cell(x, y)
        
        if isinstance(cell, MineCell):
            cell.reveal()
            self.game_over = True
            return
        
        if cell.is_revealed() or cell.is_flagged():
            return
        
        if isinstance(cell, EmptyCell):
            self._flood_fill(x, y)
        else:
            cell.reveal()
    
    def reset(self):
        self.initialized = False
        self.game_over = False
        self.game_won = True
        for y in range(self.height):
            for x in range(self.width):
                self._set_cell(x, y, EmptyCell())
    
    def _get_cell(self, x: int, y: int):
        return self.grid[y][x]
    
    def _set_cell(self, x: int, y: int, cell: Cell):
        self.grid[y][x] = cell

    def _get_safe_zone(self, x: int, y: int) -> set[tuple[int, int]]:
        """Get the safe zone (first click + 8 neighbors) to avoid placing mines."""
        safe_zone = {(x, y)}
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    safe_zone.add((nx, ny))
        return safe_zone

    def _place_mines(self, safe_zone: set[tuple[int, int]]):
        """Place mines randomly on the board, avoiding the safe zone."""
        # Get all valid positions (excluding safe zone)
        all_positions = [(x, y) for x in range(self.width) for y in range(self.height)]
        valid_positions = [pos for pos in all_positions if pos not in safe_zone]
        
        # Randomly select mine positions
        mine_positions = random.sample(valid_positions, self.num_mines)
        
        # Place mines
        for x, y in mine_positions:
            self._set_cell(x, y, MineCell())

    def _calculate_numbers(self):
        """Calculate the number of adjacent mines for each non-mine cell."""
        for y in range(self.height):
            for x in range(self.width):
                # Skip if already a mine
                if isinstance(self.grid[y][x], MineCell):
                    continue
                
                # Count adjacent mines
                mine_count = self._count_adjacent_mines(x, y)
                
                # Set appropriate cell type
                if mine_count > 0:
                    self._set_cell(x, y, NumberCell(mine_count))
                # else: keep as EmptyCell (not needded hence in the initializer we set all to EmptyCell)

    def _count_adjacent_mines(self, x: int, y: int) -> int:
        """Count the number of mines adjacent to a cell."""
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if isinstance(self._get_cell(nx, ny), MineCell):
                        count += 1
        return count

    def _get_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """Get valid neighbor coordinates for flood fill."""
        neighbors : list[tuple[int, int]] = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbors.append((nx, ny))
        return neighbors
    
    

    def _flood_fill(self, x: int, y: int):
        """Perform flood fill from the given cell to reveal all connected empty cells."""
        visited : set[tuple[int, int]] = set()
        to_visit = [(x, y)]
        
        while to_visit:
            cx, cy = to_visit.pop(0)
            
            # Skip if already visited
            if (cx, cy) in visited:
                continue
            
            visited.add((cx, cy))
            cell = self.grid[cy][cx]
            
            # Skip if flagged or already revealed
            if cell.is_flagged() or cell.is_revealed():
                continue
            
            # Reveal the cell
            cell.reveal()
            
            # Only continue flood fill if it's an empty cell (not a number)
            if isinstance(cell, EmptyCell):
                for nx, ny in self._get_neighbors(cx, cy):
                    if (nx, ny) not in visited:
                        to_visit.append((nx, ny))
            # If it's a NumberCell, we reveal it but don't add neighbors
    
    def show_board(self) -> str:
        """Return a string representation of the board."""
        result : list[str] = []
        
        # Add column numbers
        header = "   " + " ".join(f"{x:2}" for x in range(self.width))
        result.append(header)
        result.append("   " + "---" * self.width)
        
        for y in range(self.height):
            row = f"{y:2}|"
            for x in range(self.width):
                cell = self._get_cell(x, y)
                row += self._cell_display(cell) + " "
            result.append(row)
        
        return "\n".join(result)

    def _cell_display(self, cell: Cell) -> str:
        """Return display character for a cell."""
        if cell.is_flagged():
            return "F "
        
        if not cell.is_revealed():
            return "□ "
        
        if isinstance(cell, MineCell):
            return "M"
        
        if isinstance(cell, NumberCell):
            return f"{cell.get_value()} "
        
        if isinstance(cell, EmptyCell):
            return ". "
        
        return "? "

    def print_board(self):
        """Print the board to console."""
        print(self.show_board())
        print(f"\nMines: {self.num_mines}")
        print(f"Game Over: {self.game_over}")
        print(f"Game Won: {self.is_game_won()}")