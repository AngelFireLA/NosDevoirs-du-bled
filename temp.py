def tri_giga_mini(lst):
    for i in range(len(lst)):
        for j in range(len(lst) - i - 1):
            if lst[j] > lst[j + 1]: lst[j], lst[j + 1] = lst[j + 1], lst[j]
    return lst


print(tri_giga_mini([3, 2, 1, 5, 4, 5, -1, 0, 0.5, -2.5]))

