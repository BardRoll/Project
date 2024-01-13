def change_number_to_position(row, column):
    list_of_column = []
    row_number = int(row)
    for number in column.split(","):
        numbers = int(number)
        numbers = (row_number * 10) + numbers
        list_of_column.append(numbers)
    return list_of_column

print(change_number_to_position(2, "5,3,7"))