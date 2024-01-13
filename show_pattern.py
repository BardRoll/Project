import sys

try:
	import launchpad_py as launchpad
except ImportError:
	try:
		import launchpad
	except ImportError:
		sys.exit("error loading launchpad.py")

# import launchpad_py as lppy
import random
from pygame import time
import time as clock
from csv import reader
import json

# if launchpad.LaunchpadMiniMk3().Check( 1 ):
# 	lp = launchpad.LaunchpadMiniMk3()
# 	if lp.Open( 1, "minimk3" ):
# 		print("Launchpad Mini Mk3")
# 		mode = "Pro"

# Remove after test
# lp = launchpad.LaunchpadMiniMk3()
###################

class show_pattern():
    def __init__(self):
        self.csv_filename = ""
        self.pattern_list = []
        self.mini_mk3_level_dict = {1: [44, 45, 54, 55], 2: [33, 34, 35, 36, 43, 44, 45, 46, 53, 54, 55, 56, 63, 64, 65, 66], 3: [22, 23, 24, 25, 26, 27, 32, 33, 34, 35, 36, 37, 42, 43, 44, 45, 46, 47, 52, 53, 54, 55, 56, 57, 62, 63, 64, 65, 66, 67, 72, 73, 74, 75, 76, 77]}
        self.mode = ""
        self.lp = ""
        self.check_launchpad_function = 0
        self.mini_mk3_matrix_dict = {1:[column for column in range(11,19)],
                                     2:[column for column in range(21,29)],
                                     3:[column for column in range(31,39)],
                                     4:[column for column in range(41,49)],
                                     5:[column for column in range(51,59)],
                                     6:[column for column in range(61,69)],
                                     7:[column for column in range(71,79)],
                                     8:[column for column in range(81,89)]}
        self.mini_mk3_matrix = [[0],
                                [column for column in range(11,19)],
                                [column for column in range(21,29)],
                                [column for column in range(31,39)],
                                [column for column in range(41,49)],
                                [column for column in range(51,59)],
                                [column for column in range(61,69)],
                                [column for column in range(71,79)],
                                [column for column in range(81,89)]]
        self.number_of_keys = 0
        self.trials = 0
    
    def check_launchpad(self):
        if launchpad.LaunchpadPro().Check( 0 ):
            self.lp = launchpad.LaunchpadPro()
            if self.lp.Open( 0 ):
                # print("Launchpad Pro")
                self.mode = "Pro"
        elif launchpad.LaunchpadProMk3().Check( 0 ):
            self.lp = launchpad.LaunchpadProMk3()
            if self.lp.Open( 0 ):
                # print("Launchpad Pro Mk3")
                self.mode = "ProMk3"

        # experimental MK3 implementation
        # The MK3 has two MIDI instances per device; we need the 2nd one.
        # If you have two MK3s attached, its "1" for the first and "3" for the 2nd device
        elif launchpad.LaunchpadMiniMk3().Check( 1 ):
            self.lp = launchpad.LaunchpadMiniMk3()
            if self.lp.Open( 1, "minimk3" ):
                # print("Launchpad Mini Mk3")
                self.mode = "Pro"

        # experimental LPX implementation
        # Like the Mk3, the LPX also has two MIDI instances per device; we need the 2nd one.
        # If you have two LPXs attached, its "1" for the first and "3" for the 2nd device
        elif launchpad.LaunchpadLPX().Check( 1 ):
            self.lp = launchpad.LaunchpadLPX()
            if self.lp.Open( 1, "lpx" ):
                # print("Launchpad X")
                self.mode = "Pro"
                
        elif launchpad.LaunchpadMk2().Check( 0 ):
            self.lp = launchpad.LaunchpadMk2()
            if self.lp.Open( 0, "mk2" ):
                # print("Launchpad Mk2")
                self.mode = "Mk2"

        elif launchpad.LaunchControlXL().Check( 0 ):
            self.lp = launchpad.LaunchControlXL()
            if self.lp.Open( 0, "control xl" ):
                # print("Launch Control XL")
                self.mode = "XL"
                
        elif launchpad.LaunchKeyMini().Check( 0 ):
            self.lp = launchpad.LaunchKeyMini()
            if self.lp.Open( 0, "launchkey" ):
                # print("LaunchKey (Mini)")
                self.mode = "LKM"

        elif launchpad.Dicer().Check( 0 ):
            self.lp = launchpad.Dicer()
            if self.lp.Open( 0, "dicer" ):
                # print("Dicer")
                self.mode = "Dcr"

        elif launchpad.MidiFighter64().Check( 0 ):
            self.lp = launchpad.MidiFighter64()
            if self.lp.Open( 0 ):
                # print("Midi Fighter 64")
                self.mode = "MF64"

        else:
            self.lp = launchpad.Launchpad()
            if self.lp.Open():
                # print("Launchpad Mk1/S/Mini")
                self.mode = "Mk1"
        if self.mode != None:
            self.check_launchpad_function = 1
        # return self.lp
        
    
    def import_csv(self, file_path):
        self.csv_filename = file_path
    
    def load_csv(self, filename):
        pattern_list = []
        file = open(filename, "r")
        csv_reader = reader(file)
        for row in csv_reader:
            if not row:
                continue
            pattern_list.append(row)
        file.close()
        return pattern_list
    
    def csv_show(self):
        lp = self.lp
        len_pattern_list = len(self.pattern_list) # number of row
        number_of_button = len(self.pattern_list[0])
        check_position = []
        # check_while = 1
        
        # while(check_while):
        #     for round in range (1, len_pattern_list):
        #         sec = self.pattern_list[round]
        #         for position in range (number_of_button):
        #             if sec[position] == "":
        #                 continue
        #             color = sec[position]
        #             print("position = ", position, ", color = ", color)
        #             lp.LedCtrlRaw(position+11 , random.randint(0,63), random.randint(0,63), random.randint(0,63) )
        #         time.wait(1000)
        #     check_while = 0            
            # pass
        # pass
        

        for round in range (1, len_pattern_list):
            sec = self.pattern_list[round]
            for position in range (number_of_button):
                if sec[position] == "":
                    continue
                color = sec[position]
                print("position = ", position, ", color = ", color)
                lp.LedCtrlRaw(position+11 , random.randint(0,63), random.randint(0,63), random.randint(0,63) )
                if position+11 not in check_position:
                    check_position.append(position+11)
            time.wait(1000)
        time.wait(1000)
        lp.Reset()
        return check_position
    
    def show_csv(self, pattern):
        lp = self.lp
        pattern_list = pattern
        row_pattern = len(pattern_list)
        column_pattern = len(pattern_list[0])
        pattern_dict = {}
        check_position = []
        position_number = 80 # for calculate position
        
        # check sequence numbers and position of numbers
        for row in range(0, row_pattern):
            for column in range(0, column_pattern):
                position = pattern_list[row][column]                
                if position == "":
                    continue
                position = int(position)
                value = (column + 1) + position_number
                # column + 1 for update column
                # (column + 1) + 80 for change value to position number of launchpad
                pattern_dict.update({position:value})
            position_number -= 10
        
        # append position in sequence to check list
        sequence_number = 1
        len_dict = len(pattern_dict)
        while(1):
            for key in pattern_dict:
                if key == sequence_number:
                    check_position.append(pattern_dict[key])
                    sequence_number += 1
            if len(check_position) == len_dict:
                break
        
        # show pattern
        len_check = len(check_position)
        for index in range(0, len_check):
            lp.LedCtrlRaw(check_position[index] , random.randint(0,63), random.randint(0,63), random.randint(0,63) )
            time.wait(1000)
        lp.Reset()
        return check_position
    
    def random_show_sequence(self, level):
        lp = self.lp
        button_pattern = list(self.mini_mk3_level_dict[level])        
        len_button_pattern = len(button_pattern)
        check_position = []
        for round in range (0,level+2): #2
            button_position = random.choice(button_pattern)
            a = random.randint(0,63)
            b = random.randint(0,63)
            c = random.randint(0,63)
            # print("button position = ", lp.LedCtrlRaw, button_position, a,b,c)
            lp.LedCtrlRaw(button_position , a, b, c )
            check_position.append(button_position)
            button_pattern.remove(button_position)
            if round != level+1:
                time.wait(1000)
        time.wait(1000)
        lp.Reset()
        return check_position
    
    def random_show_simultaneous(self, level):
        lp = self.lp
        button_pattern = list(self.mini_mk3_level_dict[level])        
        len_button_pattern = len(button_pattern)
        check_position = []
        for round in range (0,level+2): 
            button_position = random.choice(button_pattern)
            lp.LedCtrlRaw(button_position , random.randint(0,63), random.randint(0,63), random.randint(0,63) )
            check_position.append(button_position)
            button_pattern.remove(button_position)
        time.wait(2000)
        lp.Reset()
        return check_position
    
    def change_number_to_position(self, row, column):
        list_of_num = []
        len_row = len(row)
        len_column = len(column)
        if len_row > len_column:
            for column_index in range(0, len_column):
                for row_index in range(0, len_row):
                    number = column[column_index] + (row[row_index] * 10)
                    list_of_num.append(number)
        elif len_row < len_column:
            for row_index in range(0, len_row):
                for column_index in range(0, len_column):
                    number = column[column_index] + (row[row_index] * 10)
                    list_of_num.append(number)
        else:
            for index in range(0, len_row):
                number = column[index] + (row[index] * 10)
                list_of_num.append(number)
                
        return list_of_num
    
    def split_number(self, row):
        list_of_num = []
        if len(row) == 1:
            return [int(row)]
        for number in row.split(","):
            numbers = int(number)
            list_of_num.append(numbers)
        return list_of_num
    
    def RandRow_FixColumn(self, column):
        column_list = []
        if len(column) == 1:
            result = (random.randint(1,8) * 10) + int(column)
            return result
        for number in column.split(","):
            numbers = int(number)
            numbers += (random.randint(1,8) * 10)
            column_list.append(numbers)
        return column_list
        
    
    def show_sequence(self, key, row, column, color):
        lp = self.lp
        self.number_of_keys = key
        button_matrix = [[0],
                        [column for column in range(11,19)],
                        [column for column in range(21,29)],
                        [column for column in range(31,39)],
                        [column for column in range(41,49)],
                        [column for column in range(51,59)],
                        [column for column in range(61,69)],
                        [column for column in range(71,79)],
                        [column for column in range(81,89)]]
        check_position = []
        # fix green color
        color1 = 0
        color2 = 63
        color3 = 0
        # "row" and "column" input data are string
        if row != "random": # fix row
            row_num = self.split_number(row)
            if column == "random": # random column
                for row_number in row_num:
                    for round in range(0, key): # key = number of lights 
                        button_position = random.choice(button_matrix[row_number]) # random column number
                        if color == "multi": # random color
                            color1 = random.randint(0,63)
                            color2 = random.randint(0,63)
                            color3 = random.randint(0,63)
                        lp.LedCtrlRaw(button_position, color1, color2, color3)
                        check_position.append(button_position)
                        button_matrix[row_number].remove(button_position) # ensures that the position numbers are unique
                        if round != key-1:
                            time.wait(1000)
                            
            elif column != "random": # fix column
                # fix (only one) row and fix column -> sequence depends on column number
                column_num = self.split_number(column) # data may be have this format: "1,2,3"
                column_list = self.change_number_to_position(row_num, column_num) # like: row 1 column 1 -> 11, row 2 column 3 -> 23 
                for round in range(0, key):
                    button_position = column_list[round]
                    if color == "multi": # random color
                        color1 = random.randint(0,63)
                        color2 = random.randint(0,63)
                        color3 = random.randint(0,63)
                    lp.LedCtrlRaw(button_position, color1, color2, color3)
                    check_position.append(button_position)
                    if round != key-1:
                        time.wait(1000)
                        
        elif row == "random": # random row
            if column == "random": # random column
                for round in range(0, key):
                    row_number = random.randint(1,8)
                    button_position = random.choice(button_matrix[row_number])
                    if color == "multi": # random color
                        color1 = random.randint(0,63)
                        color2 = random.randint(0,63)
                        color3 = random.randint(0,63)
                    lp.LedCtrlRaw(button_position, color1, color2, color3)
                    check_position.append(button_position)
                    button_matrix[row_number].remove(button_position)
                    if round != key-1:
                        time.wait(1000)
                        
            elif column != "random": # fix column
                # fix (only one) row and fix column -> sequence depends on column number
                column_list = self.RandRow_FixColumn(column)
                for round in range(0, key):
                    button_position = column_list[round]
                    if color == "multi": # random color
                        color1 = random.randint(0,63)
                        color2 = random.randint(0,63)
                        color3 = random.randint(0,63)
                    lp.LedCtrlRaw(button_position, color1, color2, color3)
                    check_position.append(button_position)
                    if round != key-1:
                        time.wait(1000)
        time.wait(1000)
        lp.Reset()
        return check_position
    
    def check_button_press_sequence(self, check):
        lp = self.lp
        pattern_check = check
        press_check = []        
        but_hit = len(pattern_check) * 2 # multiply 2 because lp.ButtonStateRaw() will read button when press or release
        while_loop = 1 # for break while loop
        check_position = 0
        time_used_list = []
        timer1 = clock.perf_counter() # start timer
            
        while(while_loop):
            but = lp.ButtonStateRaw() # need to read button all the time
            if but != []: # press button
                lp.LedCtrlRaw(but[0], 0, 63, 0) # show green color on button pressed
                but_hit -= 1
                if but[0] not in press_check: # but[0] can be same
                    press_check.append(but[0])
                    if press_check != [] and press_check[check_position] != pattern_check[check_position]:
                        # case: wrong button
                        timer2 = clock.perf_counter()
                        lp.LedAllOn(120) # red color show on entire launchpad panel
                        time_use = timer2 - timer1
                        time_used_list.append(time_use)
                        time_used_list.append("wrong")
                        time_used_list.append("fail: press " + str(press_check[check_position]) + ", but pattern is " + str(pattern_check[check_position]))
                        while_loop = 0 # break while loop
                        time.wait(1000)
                        break
                    check_position += 1
                if but_hit < 1:
                    # case: all buttons pressed correctly
                    timer2 = clock.perf_counter()
                    time_use = timer2 - timer1
                    time_used_list.append(time_use)
                    lp.LedAllOn(20) # green color show on entire launchpad panel
                    while_loop = 0
                    time.wait(1000)
                    break
        
        lp.Reset()
        return time_used_list
    
    def check_button_press_simultaneous(self, check):
        lp = self.lp
        pattern_check = check
        press_check = []
        timer1 = clock.perf_counter()
        print("timer1 = ", timer1)
        but_hit = len(pattern_check) * 2
        print(but_hit)
        while_loop = 1
        check_position = 0
        time_used_list = []
            
        while(while_loop):
            but = lp.ButtonStateRaw()
            if but != []:
                lp.LedCtrlRaw(but[0], 0, 63, 0)
                but_hit -= 1
                if but[0] not in press_check: # but[0] can be same
                    press_check.append(but[0])
                    press_position = press_check[check_position]
                    print("press before: ", press_check)
                    print("pattern before: ", pattern_check)
                    if press_check != [] and press_check[check_position] not in pattern_check:
                        timer2 = clock.perf_counter()
                        lp.LedAllOn(120)
                        print("Wrong button!")
                        print("timer2 = ",timer2)
                        time_used_list.append(timer2 - timer1)
                        while_loop = 0 # break while loop
                        time.wait(1000)
                        break
                    print("press position = ", press_position)
                    check_position += 1
                    pattern_check.remove(press_position)
                    print("press after: ", press_check)
                    print("pattern after: ", pattern_check)
                if but_hit < 1:
                    timer2 = clock.perf_counter()
                    # print("timer2 = ",timer2)
                    time_used_list.append(timer2 - timer1)
                    lp.LedAllOn(20)
                    while_loop = 0
                    time.wait(1000)
                    break
                print( but_hit, "event: ", but )
        return time_used_list
    
    def show_pattern_all(self):
        # print("check lp = ", self.check_launchpad_function)
        # if self.check_launchpad_function == 0:
        #     self.check_launchpad()
        #     print("activate")
        lp = launchpad.LaunchpadMiniMk3()
        self.lp = launchpad.LaunchpadMiniMk3()
        # lp = self.lp
        self.import_csv()
        if self.csv_filename != "":
            self.load_csv() # close csv!!
            # self.check_launchpad()
            # lp = self.lp
            check_position = self.csv_show()
            print("check_position = ",check_position)
            time_use = self.check_button_press_sequence(check_position)
            print("time use = ", time_use)
        else:
            print("No CSV file.")
            # self.check_launchpad()
            # lp = self.lp
            level = int(input("Enter pattern level: "))
            # for i in range(0,2):
            #     check_position = self.random_show_sequence(level)
            #     print("check_position = ",check_position)
            #     time_use = self.check_button_press_sequence(check_position)
            #     print("time use = ", time_use)
            #     lp.ButtonFlush()
            #     lp.Reset()
            check_position = self.random_show_sequence(level)
            print("check_position = ",check_position)
            time_use = self.check_button_press_sequence(check_position)
            print("time use = ", time_use)
        lp.ButtonFlush()
        lp.Reset()
        # lp.Close()
        x = {"time_use":time_use[0]}
        y = json.dumps(x)
        print(y)
        return y
