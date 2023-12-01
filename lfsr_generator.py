import random


class LFSR:
    """ Генерирует псевдослучайную последовательность по алгоритму LFSR """


    def __init__(self):
        self.__polynomial = [0, 0, 1, 0, 0, 0, 1]
        self.state = self.__generate_state(len(self.__polynomial))


    def __generate_state(self, n: int) -> list[int]:
        """ Считывает начальное состояние из файла и возвращает его """
        state = []
        for _ in range(n):
            state.append(random.randint(0, 1))
        return state
        

    def get_polynomial(self) -> list[int]:
        """ Возвращает полином """
        return self.__polynomial
    
    
    def get_state(self):
        """ Возвращает начальное состояние """
        return self.state
       

    def __calc_new_bit(self, new_state: list) -> int:
        """ Считает и возвращет бит для получения нового состояния """
        new_bit = 0
        polynomial = self.get_polynomial()
        for i in range(len(polynomial)):
            if polynomial[i] == 1:
                 new_bit ^= new_state[i]
        return new_bit
    
    
    def generate(self, n: int = 127) -> list[int]:
        """ Генерирует и возвращает псевдослучайную последовательность """
        result, new_state = [], []
        result.append(self.state[-1])
        new_state = self.state[:-1]
        new_state.insert(0, self.__calc_new_bit(self.state))
        for _ in range(n - 1):
            result.append(new_state[-1])
            new_bit = self.__calc_new_bit(new_state)
            new_state = new_state[:-1]
            new_state.insert(0, new_bit)
        return result
    