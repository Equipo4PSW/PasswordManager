def cyclicIndex(current, end, increment):
    start = 3
    end = end-1 + start
    newIndex = current + increment

    if newIndex > end:
        return start
    elif newIndex <= start:
        return end
    return newIndex


current_index = cyclicIndex(12, 10, 1)
print(current_index)
# for _ in range(20):  # Imprime los próximos 20 índices cíclicos
#     current_index = cyclicIndex(current_index, 10, -1)
#     print(current_index)

