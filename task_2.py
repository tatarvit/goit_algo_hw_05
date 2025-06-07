# Завдання 2
# Реалізуйте двійковий пошук для відсортованого масиву з дробовими числами.
# Написана ф-ція для бінарного пошуку повина повертати кортеж, де першим елементом
# є кількість ітерацій, потрібних для знаходження елемента.
# Другим елементом має бути "верхня межа" - це найменший елемент, який є більшим
# або рівним заданому значенню
# ==============================================================================================
def binary_search_upper_bound(arr, goal):
    left, right = 0, len(arr) - 1
    iterations = 0
    upper_bound = None

    print(f"Початковий масив: {arr}")
    print(f"Цілюве значення: {goal}")
    print("Початок пошуку...\n")

    while left <= right:
        iterations += 1
        mid = (left + right) // 2
        print(f"Ітерація {iterations}: ")
        print(f"   Ліва межа: {left}, Права межа: {right}")
        print(f"   Середина (index {mid})={arr[mid]}")

        if arr[mid] < goal:
            print(f"   {arr[mid]} < {goal}, рухаємося вправо")
            left = mid + 1
        else:
            print(f"   {arr[mid]} >= {goal}, можлива верхня межа")
            upper_bound = arr[mid]
            right = mid - 1
        print()

    print(f"Результат: ітерацій => {iterations}, верхня межа => {upper_bound}")
    return iterations, upper_bound


# Тест
arr = [0.1, 0.5, 1.2, 2.3, 3.3, 4.8]
goal = 1.0
result = binary_search_upper_bound(arr, goal)
print(result)
