from show_pattern import show_pattern
import json
import sys
import random
def main(data_from_django):    
    show = show_pattern()
    show.check_launchpad()
    
    key = int(data_from_django[0])
    end_key = int(data_from_django[1])
    row = data_from_django[2]
    column = data_from_django[3]
    color = data_from_django[4]
    trials = int(data_from_django[5])
    csv_name = data_from_django[6]
    check_break = 0
    result = []
    if csv_name[0] != "-":
        for i in range(0, len(csv_name)):
            result_level = []
            for trial in range(0,2):
                filename = "D:/66/1/ProjectPrep/Launchpad/web_server/myapp/media/" + csv_name[i]
                load = show.load_csv(filename)
                check = show.show_csv(load)
                res = show.check_button_press_sequence(check)
                round_time = round(res[0], 2)
                key = len(check)
                if res[len(res)-2] == "wrong":
                    result_trial = [key, check, trial+1, round_time, res[len(res)-1], csv_name[i]]
                    result_level.append(result_trial)
                    check_break = 1
                    break
                else:
                    result_trial = [key, check, trial+1, round_time, "pass", csv_name[i]]
                    result_level.append(result_trial)
            result.append(result_level)
            if check_break == 1:
                break
    else:            
        levels = end_key - key + 1
        if levels == 0: # case: only one level
            levels = 1
        for level in range(0, levels):
            result_level = []
            show.lp.LedCtrlString( "LV" + str(level+1), 0, 63, 0, -1, waitms = 50 )
            for trial in range(0, trials):
                check = show.show_sequence(key,row,column,color)
                res = show.check_button_press_sequence(check)
                round_time = round(res[0], 2)
                # result_trial = [key, check, trial+1, round_time]
                # result_level.append(result_trial)
                if res[len(res)-2] == "wrong": # เพิ่ม pass, fail ใน result ด้วย???
                    result_trial = [key, check, trial+1, round_time, res[len(res)-1]]
                    result_level.append(result_trial)
                    check_break = 1
                    break
                else:
                    result_trial = [key, check, trial+1, round_time, "pass"]
                    result_level.append(result_trial)
            result.append(result_level)
            key += 1
            if check_break == 1:
                break
    # print(result)
    sys.stdout.write(json.dumps(result))
    
    # random_data = data_from_django[0]
    # level = data_from_django[1]
    # round = data_from_django[2]
    # csv_name = data_from_django[3]
    
    # show random sequence
    # if random_data == "sequence":
    #     random_level = random.randint(1,3)
    #     check_position = show.random_show_sequence(random_level)
    #     # print("check_position = ",check_position)
    #     time_use = show.check_button_press_sequence(check_position)
    #     show.lp.Reset()
    #     # print("time use = ", time_use[0])
    #     result = {"time_use":str(time_use[0])}
    #     sys.stdout.write(json.dumps(result))
    # elif level > 0 and round > 0:
    #     for turns in range(0, round):
    #         pass
    
    # lp = launchpad.LaunchpadMiniMk3()
    # self.lp = launchpad.LaunchpadMiniMk3()
    # # lp = self.lp
    # self.import_csv()
    # if self.csv_filename != "":
    #     self.load_csv() # close csv!!
    #     # self.check_launchpad()
    #     # lp = self.lp
    #     check_position = self.csv_show()
    #     print("check_position = ",check_position)
    #     time_use = self.check_button_press_sequence(check_position)
    #     print("time use = ", time_use)
    # else:
    #     print("No CSV file.")
    #     # self.check_launchpad()
    #     # lp = self.lp
    #     level = int(input("Enter pattern level: "))
    #     # for i in range(0,2):
    #     #     check_position = self.random_show_sequence(level)
    #     #     print("check_position = ",check_position)
    #     #     time_use = self.check_button_press_sequence(check_position)
    #     #     print("time use = ", time_use)
    #     #     lp.ButtonFlush()
    #     #     lp.Reset()
    #     check_position = self.random_show_sequence(level)
    #     print("check_position = ",check_position)
    #     time_use = self.check_button_press_sequence(check_position)
    #     print("time use = ", time_use)
    # lp.ButtonFlush()
    # lp.Reset()
    # # lp.Close()
    # x = {"time_use":time_use[0]}
    # y = json.dumps(x)
    # print(y)
    # return y
    
if __name__ == '__main__':
    django_data = input()
    json_data = json.loads(django_data)
    run = main(json_data)
    