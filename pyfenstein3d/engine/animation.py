from numpy import interp

class Animation:
    def __init__(self, time: float, on_animate=None, on_animate_end=None):
        self.__total_time = time
        self.__on_animate = on_animate
        self.__on_animate_end = on_animate_end
        self.__time = 0
        self.__factor = 0
        self.__is_animating = False

    @property
    def total_time(self):
        return self.__total_time;

    @property
    def time(self):
        return self.__time;

    @property
    def is_animating(self):
        return self.__is_animating;

    @property
    def factor(self):
        return self.__factor;

    def start(self, at: int = 0):
        self.__time = at
        self.__is_animating = True

    def update(self, delta_time: float):
        if self.__is_animating:
            self.__time += delta_time
            self.__factor =  self.__time / self.__total_time
            self.__factor = self.__factor if self.__factor <= 1 else 1;
            if self.__on_animate is not None:
                self.__on_animate(self.__factor)
            if self.__factor >= 1:
                self.__is_animating = False
                if self.__on_animate_end is not None:
                    self.__on_animate_end()
        else:
            self.__factor = 0
