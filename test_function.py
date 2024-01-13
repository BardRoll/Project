# list_button_position = [i for i in range(11,90) if i % 10 != 9 and i % 10 != 0]
# inp = input("Input: ")
# level = int(inp)
# dict_list = {1: [44, 45, 54, 55], 2: [33, 34, 35, 36, 43, 44, 45, 46, 53, 54, 55, 56, 63, 64, 65, 66]}
# print(dict_list[level])

def generate_output(n):
    """
    Generate a list of numbers based on the given input.

    Args:
        n (int): The input number.

    Returns:
        list: A list of numbers.

    Examples:
        >>> generate_output(1)
        [44, 45, 54, 55]
        >>> generate_output(2)
        [33, 34, 35, 36, 43, 44, 45, 46, 53, 54, 55, 56, 63, 64, 65, 66]
        >>> generate_output(3)
        [22, 23, 24, 25, 26, 27, 32, 33, 34, 35, 36, 37, 42, 43, 44, 45, 46, 47, 52, 53, 54, 55, 56, 57, 62, 63, 64, 65, 66, 67, 72, 73, 74, 75, 76, 77]
    """
    output = []
    for i in range(n, 0, -1):
        for j in range(n, 0, -1):
            output.append(int(str(i) + str(j)))
            output.append(int(str(i) + str(n + j)))
            output.append(int(str(n + i) + str(j)))
            output.append(int(str(n + i) + str(n + j)))
    return output

# Test the function
# print(generate_output(1))
# print(generate_output(2))
# print(generate_output(3))


from show_pattern import show_pattern
key = 2
row = "4,5"
column = "2"
color = "single"
check_break = 0
test = show_pattern()
test.check_launchpad()
result = []
for level in range(0,2):
    result_level = []
    test.lp.LedCtrlString( "LV" + str(level+1), 0, 63, 0, -1, waitms = 50 )
    for trial in range(0,2):
        check = test.show_sequence(key,row,column,color)
        res = test.check_button_press_sequence(check)
        round_time = round(res[0], 2)
        result_trial = [key, check, round_time]
        result_level.append(result_trial)
        print(res)
        if res[0] == 0:
            check_break = 1
            break
    result.append(result_level)
    key += 1
    if check_break == 1:
        break
print(result)
# test.import_csv()
# test.load_csv("D:/66/1/ProjectPrep/Launchpad/web_server/myapp/media/file/test_csv.csv")
# print(test.show_csv())
# print(test.pattern_list)