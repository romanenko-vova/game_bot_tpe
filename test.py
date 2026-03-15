

lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
tp = (1, 2, 3, 4, 5, 6, 7, 8, 9)
print(lst.__sizeof__())
print(tp.__sizeof__())
lst = [x for x in range(1000000)]
tp = (x for x in range(1000))
print(lst.__sizeof__())
print(tp.__sizeof__())

dic = {'a': [1, 2, 3, 4, 5, 6, 7, 8, 9], 'c': [2, 3, 4, 5, 6, 7, 8, 9, 10], 'e': 'f', 'g': 'h', 'i': 'j'}
print(dic.__sizeof__())
