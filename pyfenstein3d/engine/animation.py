from numpy import interp

class Animation:
    def __init__(self, time: float, on_animate=None, on_animate_end=None):
        self.__total_time = time
        self.__on_animate = on_animate
        self.__on_animate_end = on_animate_end
        self.__time = 0
        self.__factor = 0
        self.__is_animating = False

    def start(self):
        self.__time = 0
        self.__is_animating = True

    def animate(self, delta_time: float):
        if self.__is_animating:
            self.__time += delta_time
            self.__factor =  self.__time / self.__total_time
            if self.__on_animate is not None:
                self.__on_animate(self.__factor)
            if self.__factor >= 1:
                self.__is_animating = False
                if self.__on_animate_end is not None:
                    self.__on_animate_end()
