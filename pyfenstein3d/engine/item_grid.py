from .item import Item


class ItemGrid():
    def __init__(self, items: []):
        self.__max_x = max(map(lambda i: i.block_x, items)) + 1
        self.__max_y = max(map(lambda i: i.block_y, items)) + 1
        grid = [None] * self.__max_y * self.__max_x
        self.__grid = [grid[n:n+self.__max_y]
                       for n in range(0, len(grid), self.__max_y)]
        for item in items:
            self.__grid[item.x][item.y] = item

    def get_item(self, block_x, block_y) -> Item:
        if block_x < self.max_x and block_y < self.max_y:
            return self.__grid[block_x][block_y]
        return None

    @property
    def max_x(self):
        return self.__max_x

    @property
    def max_y(self):
        return self.__max_y
