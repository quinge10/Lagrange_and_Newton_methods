"""
Нахождение и построение интерполирующего многочлена
методами Лагранжа и Ньютона

Created by: Andrew Ushakov
10.04.2017

"""

import math
import numpy as np
from matplotlib import pyplot as plt


class Newton:
    """ Рассчет интерполяционного многочлена Ньютона """

    def __init__(self, x, f):
        """ 
        Задаем функцию разделенной разности нулевого порядка.
        Задаем точки, в которых проводится интерполяция многочлена.
        
        :param x: float
                  Аргументы функции
        :param f: func
                  Заданная функция
        """
        self.__f_0 = f
        self.__x = x
        self.__y = [self.__f(x) for x in self.__x]

    def __f(self, *x):
        """ Функция разделенной разности
        
        :param x: float
                  Аргумент функции
        :return: float
                 Значение функции в точках
        """

        if len(x) == 1:  # Функция нулевого порядка совпадает
            return self.__f_0(x[0])  # со значением функции в точках
        *x_1, tail = x
        nose, *x_2 = x
        return (self.__f(*x_1) - self.__f(*x_2)) / (x_1[0] - tail)

    def calculate(self):
        """ Вычисляем интерполяционный многочлен
         
         Используем метод Ньютона
        :return: func
                 Функция интерполирующая заданную
        """

        def newton(x):
            res = self.__f(self.__x[0])  # Результат функции

            for i in range(1, len(self.__x)):
                left = 1  # Тут храним перемножение скобок вида (x - x_i)
                for j in range(i):
                    left *= (x - self.__x[j])

                # Умножаем на f(x_0, x_1, ..., x_i) и прибавляем результат
                res += left * self.__f(*self.__x[:i+1])

            return res

        return newton


class Lagrange:
    """ Рассчет интерполяционного многочлена Лагранжа """

    def __init__(self, x, f):
        """ Задаем точки, в которых проводится интерполяция многочлена """
        self.__x = x
        self.__y = [f(x) for x in self.__x]

    def __l(self, x, i):
        res = 1
        for j in range(len(self.__x)):
            if j != i:
                res *= (x - self.__x[j]) / (self.__x[i] - self.__x[j])
        return res

    def calculate(self):
        """ Вычисляем интерполяционный многочлен
        
        Используем метод Лагранжа
        :return: func
                 Функция интерполирующая заданную
        """

        def lagrange(x):
            res = 0
            for i in range(len(self.__x)):
                res += self.__y[i] * self.__l(x, i)
            return res

        return lagrange


class Interface:
    """ Отображение функций на графике """

    def draw(self, min_x, max_x, *func):
        """ Построение графика функций
        
        :param min_x: float
                      Левая граничная точка на оси Х
        :param max_x: float
                      Правая граничная точка по оси Х
        :param func: func
                     Функции, которые отображаются координатной плоскости 
        :return: 
        """

        for f in func:
            x = np.linspace(min_x, max_x, 100)  # Зададим точки по которым
            y = [f(x_i) for x_i in x]           # будем рисовать график
            plt.plot(x, y, '--', linewidth=2, label=f.__name__)

        plt.grid()
        plt.legend(bbox_to_anchor=(0., 1.02, 1., 0.102), loc=3,
                   ncol=2, mode="expand", borderaxespad=0.)
        plt.show()

if __name__ == '__main__':

    def f(x): return math.log(x) + x

    cls = Newton([0.1, 0.5, 1.1, 1.3], f)
    newton = cls.calculate()

    cls = Lagrange([0.1, 0.5, 0.9, 1.3], f)
    lagrange = cls.calculate()

    interface = Interface()
    interface.draw(0.1, 1.3, f, newton)
    interface.draw(0.1, 1.3, f, lagrange)

    print("\n\nАбсолютная погрешность интерполяции по Лагранжу составляет:",
          abs(abs(lagrange(0.8)) - abs(f(0.8))), end='\n\n')

    print("Абсолютная погрешность интерполяции по Ньютону составляет:",
          abs(abs(newton(0.8)) - abs(f(0.8))))


