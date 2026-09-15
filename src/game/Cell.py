import abc
from dataclasses import dataclass

@dataclass
class ActionResult:
    """Class representing the result of an action on a cell."""
    exploded: bool = False 
    revealed: bool = False
    flagged: bool = False
    already_revealed: bool = False  #Added to avoid the ai farming bia re-revealing tiles.


class Cell(metaclass=abc.ABCMeta):
    """Interface for a cell in the game grid."""

    @abc.abstractmethod
    def is_revealed(self) -> bool:
        """Check if the cell has been revealed."""
        pass

    @abc.abstractmethod
    def is_flagged(self) -> bool:
        """Check if the cell is flagged."""
        pass

    @abc.abstractmethod
    def reveal(self) -> ActionResult:
        """Reveal the cell."""
        pass

    @abc.abstractmethod
    def flag(self) -> ActionResult:
        """Flag the cell as a potential mine."""
        pass

@Cell.register
class EmptyCell(Cell):
    """Concrete implementation of an empty cell."""

    def __init__(self):
        self._revealed = False
        self._flagged = False

    def is_revealed(self) -> bool:
        return self._revealed

    def reveal(self) -> ActionResult:
        if self._revealed:
            return ActionResult(already_revealed=True)
        if self._flagged:
            self._flagged = False 
        self._revealed = True
        return ActionResult(revealed=True)

    def is_flagged(self) -> bool:
        return self._flagged

    def flag(self) -> ActionResult:
        if self._revealed:
            return ActionResult(already_revealed=True)
        if self._flagged:
            self._flagged = False
            return ActionResult(flagged=False)
        else:
            self._flagged = True
            return ActionResult(flagged=True)

@Cell.register    
class MineCell(Cell):
    """Concrete implementation of a mine cell."""

    def __init__(self):
        self._revealed = False
        self._flagged = False

    def is_revealed(self) -> bool:
        return self._revealed

    def reveal(self) -> ActionResult:
        if self._flagged:
            self._flagged = False
        self._revealed = True
        return ActionResult(exploded=True)
    
    def is_flagged(self) -> bool:
        return self._flagged

    def flag(self) -> ActionResult:
        if self._flagged:
            self._flagged = False
            return ActionResult(flagged=False)
        else:
            self._flagged = True
            return ActionResult(flagged=True)

@Cell.register        
class NumberCell(Cell):
    """Concrete implementation of a number cell."""

    def __init__(self, value: int):
        self._value = value
        self._revealed = False
        self._flagged = False

    def is_revealed(self) -> bool:
        return self._revealed
    
    def is_flagged(self) -> bool:
        return self._flagged

    def get_value(self) -> int:
        return self._value

    def reveal(self) -> ActionResult:
        if self._revealed:
            return ActionResult(already_revealed=True)
        self._revealed = True
        return ActionResult(revealed=True)

    def flag(self) -> ActionResult:
        if self._revealed:
            return ActionResult(already_revealed=True)
        if self._flagged:
            self._flagged = False
            return ActionResult(flagged=False)
        else:
            self._flagged = True
            return ActionResult(flagged=True)

Cell.register(EmptyCell)
Cell.register(MineCell)
Cell.register(NumberCell)
