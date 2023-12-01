import time
import random
from lfsr_generator import LFSR


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        number, count_iter = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        save_result(number, count_iter, execution_time)
        return number, count_iter
    return wrapper


def save_result(number: int, count_itter: int, time: float):
    """ Сохраняет полученные результаты в файл """
    file_result = "result.txt"
    with open(file_result, "w", encoding="utf-8") as file_out:
        print(f"{number}\n{count_itter}\n{time:.5f}", file=file_out)


class PRIME_NUMBER_ERROR(Exception):
    pass


class PRIME_NUMBER:


    def __init__(self, filename: str):
        self.n, self.p = self.__load_attrs(filename)


    def __load_attrs(self, filename: str) -> tuple[int, float]:
        """ Загружает и возвращает входные данные из файла: количество двоичных разрядов
         и вероятность признать составное число простым """
        try:
            with open(filename, "r", encoding="utf-8") as file_in:
                n = int(file_in.readline().rstrip())
                p = float(file_in.readline())
        except FileNotFoundError:
            raise PRIME_NUMBER_ERROR(f"Невозможно открыть файл: '{filename}'")
        except ValueError:
            raise PRIME_NUMBER_ERROR("Невозможно перевести строку в число")
        else: 
            if not (n > 2):
                raise PRIME_NUMBER_ERROR("Разраядность числа должна быть строго больше единицы")
            if p > 1 or p < 0:
                raise PRIME_NUMBER_ERROR("Неверно задана вероятность ошибки")
        return n, p


    def __get_birnary_sequence(self) -> list[int]:
        """ Генерирует и возвращает двоичную последовательность """
        G = LFSR()
        sequence = G.generate(self.n)
        sequence[0] = 1; sequence[self.n - 1] = 1
        return sequence


    def __pre_test(self, number: int) -> bool:
        """ Предварительное тестирование, на деление на все простые числа меньших 256 """
        prime_numbers = [
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79,
            83, 89,97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167,
            173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251
        ]
        for i in prime_numbers:
            if i != number and number % i == 0:
                return False
        return True

    
    def __lehmann_test(self, number: int, k: int = 10) -> bool:
        """ Тест Леманна """
        probability_error, power_error = 0, 0
        for _ in range(k):
            a = random.randint(2, number - 1)
            t = pow(a, (number - 1) // 2, number)
            if abs(t) == 1:
                power_error += 1
                probability_error = 0.5 ** (power_error)
        if probability_error <= self.p:
            return True
        else:
            return False


    @timer
    def generate(self):
        """ Генерирует число и возвращает его с количеством итераций основного цикла """
        count_iter = 0
        lehmann_test = False
        while not lehmann_test:
            pre_test = False
            while not pre_test:
                count_iter += 1
                birnary_sequence = "".join(str(i) for i in self.__get_birnary_sequence())
                number = int(birnary_sequence, base=2)
                pre_test = self.__pre_test(number)
            lehmann_test= self.__lehmann_test(number)
        return number, count_iter