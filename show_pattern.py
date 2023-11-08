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

if launchpad.LaunchpadMiniMk3().Check( 1 ):
	lp = launchpad.LaunchpadMiniMk3()
	if lp.Open( 1, "minimk3" ):
		print("Launchpad Mini Mk3")
		mode = "Pro"

# Remove after test
# lp = launchpad.LaunchpadMiniMk3()
###################

class show_pattern():
    def __init__(self):
        self.csv_filename = ""
        self.pattern_list = []
        # self.customized = number
        self.mini_mk3_level_dict = {1: [44, 45, 54, 55], 2: [33, 34, 35, 36, 43, 44, 45, 46, 53, 54, 55, 56, 63, 64, 65, 66], 3: [22, 23, 24, 25, 26, 27, 32, 33, 34, 35, 36, 37, 42, 43, 44, 45, 46, 47, 52, 53, 54, 55, 56, 57, 62, 63, 64, 65, 66, 67, 72, 73, 74, 75, 76, 77]}
    
    def import_csv(self):
        self.csv_filename = input("Enter csv filename: ")
    
    def load_csv(self):
        # filename = input("Enter CSV filename: ")        
        # if filename == "":
        #     return "No CSV file"
        filename = self.csv_filename
        file = open(filename, "r")
        csv_reader = reader(file)
        for row in csv_reader:
            if not row:
                continue
            self.pattern_list.append(row)
        # return self.pattern_list
    
    def csv_show(self):
        len_pattern_list = len(self.pattern_list) # บอกว่ามีกี่ row
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
                check_position.append(position)
            time.wait(1000)
        time.wait(1000)
        lp.Reset()
        return check_position
    
    def random_show_sequence(self, level):
        button_pattern = list(self.mini_mk3_level_dict[level])        
        len_button_pattern = len(button_pattern)
        check_position = []
        for round in range (0,3):
            button_position = random.choice(button_pattern)
            lp.LedCtrlRaw(button_position , random.randint(0,63), random.randint(0,63), random.randint(0,63) )
            check_position.append(button_position)
            button_pattern.remove(button_position)
            if round != 2:
                time.wait(1000)
        time.wait(1000)
        lp.Reset()
        return check_position
    
    def check_button_press_sequence(self, check):
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
                    if press_check != [] and press_check[check_position] != pattern_check[check_position]:
                        timer2 = clock.perf_counter()
                        lp.LedAllOn(120)
                        print("Wrong button!")
                        print("timer2 = ",timer2)
                        time_used_list.append(timer2 - timer1)
                        while_loop = 0 # break while loop
                        break
                    check_position += 1
                if but_hit < 1:
                    timer2 = clock.perf_counter()
                    print("timer2 = ",timer2)
                    time_used_list.append(timer2 - timer1)
                    lp.LedAllOn(20)
                    while_loop = 0
                    time.wait(1000)
                    break
                print( but_hit, "event: ", but )
            time.wait( 5 )
        return time_used_list
        

# Start test location
# pattern_design.csv
print("start")
# filename = input("Enter csv filename: ")
test = show_pattern()
test.import_csv()
# print(test.load_csv())
# test.load_csv()
# test.csv_show()
check_position = test.random_show_sequence(2)
check_press = test.check_button_press_sequence(check_position)
# print(test.pattern_list)
lp.ButtonFlush()
lp.Reset() # turn all LEDs off
lp.Close() # close the Launchpad (will quit with an error due to a PyGame bug)
print(check_position)
print(check_press)

# End test location