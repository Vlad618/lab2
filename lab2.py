list=[1, 8, 5, 9, 188, 1532, 67, 52,'a','n','h','d','e','b','g','i','l','v']
list_str=[x for x in list if isinstance(x, str)]
list_int=[x for x in list if isinstance(x, int)]
list_int.sort() # сортує список
list_str.sort() # сортує список
list_sort=list_int.copy() # повертає копію списку
list_sort.extend(list_str) # об'єднує списки
list_2=[]
for n in list_int:
    if n%2==0:
        list_2.append(n) # добавляє елемент в кінець списку
list_STR=[]
for x in list_str:
    list_STR.append(x.upper())
print('Початковий список:',list) # виводить початковий список
print('Сортований список:',list_sort) # виводить відсортований список
print('Список кратних 2:',list_2) # виводить список кратних 2
print('Список капсом:',list_STR) # виводить список капсом