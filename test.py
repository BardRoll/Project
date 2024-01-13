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

if launchpad.LaunchpadMiniMk3().Check( 1 ):
	lp = launchpad.LaunchpadMiniMk3()
	if lp.Open( 1, "minimk3" ):
		print("Launchpad Mini Mk3")
		mode = "Pro"
# if mode != "XL" and mode != "LKM" and mode != "Dcr":

# list_100 = [i for i in range(1,101)]

def pattern(level):
    if level == 1:
        pass

# list_2x2 = [44, 45, 54, 55]
# list_4x4 = [33, 34, 35, 36, 43, 44, 45, 46, 53, 54, 55, 56, 63, 64, 65, 66]

list_button_position = [i for i in range(11,90) if i % 10 != 9 and i % 10 != 0]
inp = input("Input: ")
level = int(inp)
dict_list = {1: [44, 45, 54, 55], 2: [33, 34, 35, 36, 43, 44, 45, 46, 53, 54, 55, 56, 63, 64, 65, 66], 3: [22, 23, 24, 25, 26, 27, 32, 33, 34, 35, 36, 37, 42, 43, 44, 45, 46, 47, 52, 53, 54, 55, 56, 57, 62, 63, 64, 65, 66, 67, 72, 73, 74, 75, 76, 77]}
pattern = dict_list[level]
# lp.LedCtrlString( "LEVEL" + inp, 0, 63, 0, -1, waitms = 50 )
lp.LedCtrlString( inp, 0, 63, 0, -1, waitms = 50 )
# time.wait(5)

j = 1
x = j
# for i in range (1, 5):
#     lp.LedCtrlRaw( j, random.randint(0,63), random.randint(0,63), random.randint(0,63) )
#     j += 1
#     time.wait(1000)

for_range = (level*level)+3
# or
# for_range = random.randint(0,(level*level)+3)
butHit = for_range*2-2
pattern_check = []
press_check = []
m = 0

time_used_list = []
for an in range (1,5):
    print("loop = ", an)
    pattern = list(dict_list[level])
    print("pattern = ", pattern)
    print("dict = ", dict_list[level])
    j = 1
    for_range = (level*level)+3
    # or
    # for_range = random.randint(0,(level*level)+3)
    butHit = for_range*2-2 # lp.ButtonStateRaw() will read button when push or release
    pattern_check = []
    press_check = []
    check_position = 0
    check_loop = 1
    while(check_loop):
        if j != for_range:
            for i in range (1, for_range):
                k = random.choice(pattern)
                print(k)
                lp.LedCtrlRaw(k , random.randint(0,63), random.randint(0,63), random.randint(0,63) )
                j += 1
                pattern.remove(k)
                pattern_check.append(k)
                # time.wait(1000)
            time.wait(1000)
            lp.Reset()
            timer1 = clock.perf_counter()
            print("timer1 = ", timer1)
        else:
            but = lp.ButtonStateRaw()
            print(but)
            if but != []:
                lp.LedCtrlRaw(but[0], 0, 63, 0)
                butHit -= 1
                if but[0] not in press_check:
                    press_check.append(but[0])
                    if press_check != [] and press_check[check_position] != pattern_check[check_position]:
                        timer2 = clock.perf_counter()
                        lp.LedAllOn(120)
                        print("Wrong button!")
                        print("timer2 = ",timer2)
                        time_used_list.append(timer2 - timer1)
                        check_loop = 0 # break while loop
                        break
                    check_position += 1
                if butHit < 1:
                    timer2 = clock.perf_counter()
                    print("timer2 = ",timer2)
                    time_used_list.append(timer2 - timer1)
                    lp.LedAllOn(20)
                    time.wait(1000)
                    break
                print( butHit, "event: ", but )
            time.wait( 5 )
    if check_loop == 0: # break for loop
        time.wait(1000)
        break
    lp.Reset()
    


# while(1):
#     if j != for_range:
#         for i in range (1, for_range):
#             k = random.choice(pattern)
#             print(k)
#             lp.LedCtrlRaw(k , random.randint(0,63), random.randint(0,63), random.randint(0,63) )
#             j += 1
#             pattern.remove(k)
#             pattern_check.append(k)
#             # time.wait(1000)
#             time.wait(500)
#         lp.Reset()
#         timer1 = clock.perf_counter()
#         print("timer1 = ", timer1)
#     else:
#         but = lp.ButtonStateRaw()
#         if but != []:
#             lp.LedCtrlRaw(but[0], 0, 63, 0)
#             butHit -= 1
#             if but[0] not in press_check:
#                 press_check.append(but[0])
#                 if press_check != [] and press_check[m] != pattern_check[m]:
#                     timer2 = clock.perf_counter()
#                     lp.LedAllOn(20)
#                     print("Wrong button!")
#                     print("timer2 = ",timer2)
#                     break
#                 m += 1
#             if butHit < 1:
#                 timer2 = clock.perf_counter()
#                 lp.LedAllOn(127)
#                 print("timer2 = ",timer2)
#                 break
#             print( butHit, "event: ", but )
#         time.wait( 5 )

# time_used = timer2 - timer1
print("press_check = ", press_check)
print("Time used = ", sum(time_used_list))
print("bye")


lp.ButtonFlush()
lp.Reset() # turn all LEDs off
lp.Close() # close the Launchpad (will quit with an error due to a PyGame bug)


 
# # การเชื่อมต่อ Launchpad Mini MK3
# if lp.Open(0):
#     print("Launchpad Mini MK3 พร้อมทำงาน")
# else:
#     print("ไม่สามารถเชื่อมต่อ Launchpad Mini MK3 ได้")
# lp.Check(0)
# lp.LedSetLayout(0) # Sets the button layout to "Session" mode.
# lp.LedSetMode(1) 
# lp.LedCtrlRaw(0, 1, 10)
# lp.LedCtrlPulseByCode(0, 256)
# lp.LedAllOn(0)
# lp.Close()
# print("here")





