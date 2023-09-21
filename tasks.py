#________________________________1
from random import randint

input("Нажмите enter для старта игры")
print("Угадайте число от 1 до 10")
guess_number = str(randint(1,10))
entered = input()
while entered!=guess_number:
    entered = input("Вы не угадали попробуйте снова: ")
else:
    print('Правильно!')

#_________________________________2
print()
number = int(input("Введите число: "))
if number%2 ==0:
    print(number,"простое число")
else:
    print(number,"не является простым числом")

#________________________________3

print()
n = int(input("Введите диапозон: "))
for i in range(n+1):
    if i%2==0:
        print(i,"является простым числом")

#________________________________4
print()
for i in range(1,10):
    for j in range(1,10):
        res = f'{j}*{i}={i*j}'
        if len(res)!=6:
            res+=' |'
        else:
            res+='|'
        print(res,end=' '*2)
    print('',end='\n')
    print('‾'*79)

