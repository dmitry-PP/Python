from decimal import Decimal
import math

def get_number(msg: str = ''): return Decimal(input(msg).replace(',','.'))

operations = {
    '1': lambda: f'Результат = {get_number("Введите первое число: ") + get_number("Введите второе число: ")}',
    '2': lambda:f'Результат = {get_number("Введите первое число: ")-get_number("Введите второе число: ")}',
    '3': lambda:f'Результат = {get_number("Введите первое число: ")*get_number("Введите второе число: ")}',
    '4': lambda:f'Результат = {get_number("Введите первое число: ")/get_number("Введите второе число: ")}',
    '5': lambda:f'Результат = {get_number("Введите число: ")**get_number("Введите N-степень: ")}',
    '6': lambda:f'Результат = {math.sqrt(get_number("Введите число: "))}',
    '7': lambda:f'Результат = {math.factorial(int(get_number("Введите число: ")))}',
    '8': lambda:f'Результат = {math.sin(math.radians(get_number("Введите градусы: ")))}',
    '9': lambda:f'Результат = {math.cos(math.radians(get_number("Введите градусы: ")))}',
    '10': lambda:f'Результат = {math.tan(math.radians(get_number("Введите градусы: ")))}',
}

def getMenu():
    print()
    print("__________MENU__________")
    print("1. Сложить 2 числа")
    print("2. Вычесть первое из второго")
    print("3. Перемножить два числа")
    print("4. Разделить первое на второе")
    print("5. Возвести в степень N первое число")
    print("6. Найти квадратный корень из числа")
    print("7. Найти факториал из числа")
    print("8. Найти sin (градусы)")
    print("9. Найти cos (градусы)")
    print("10. Найти tan (градусы)")
    print("________________________")
    print()

def request():
    getMenu()
    return input("Введите номер действия: ")


while (operator:=request()) != '':
    if (op:=operations.get(operator,None)) is None:
        print('Такого действия нет')
        continue
    try:
        print(op())
    except ZeroDivisionError:
        print("На ноль делить нельзя!")
    except:
        print("Ошибка, повторите попытку")