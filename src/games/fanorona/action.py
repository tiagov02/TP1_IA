class FanoronaAction:
    """
    a connect 4 action is simple - it only takes the value of the column to play
    """
    __initial_x: int
    __initial_y: int
    __final_x: int
    __final_y: int

#todo : new type of action
    def __init__(self, initial_x: int, initial_y:int, final_x:int, final_y:int):
        self.__initial_x = initial_x
        self.__initial_y = initial_y
        self.__final_x = final_x
        self.__final_y = final_y

    def get_initial_x(self):
        return self.__initial_x

    def get_initial_y(self):
        return self.__initial_y

    def get_final_x(self):
        return self.__final_x

    def get_final_y(self):
        return self.__final_y

    def get_difference_x(self):
        return self.__initial_x - self.__final_x
    def get_difference_y(self):
        return  self.__initial_y - self.__final_y