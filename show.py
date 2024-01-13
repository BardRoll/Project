from show_pattern import show_pattern
import json
import sys
import os
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
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    media_path = os.path.join(BASE_DIR, 'Launchpad', 'web_server', 'myapp', 'media')
    if csv_name[0] != "-":
        # case: use csv file
        for i in range(0, len(csv_name)):
            result_level = []
            for trial in range(0,2):
                # filename = "D:/66/1/ProjectPrep/Launchpad/web_server/myapp/media/" + csv_name[i]
                filename = os.path.join(media_path, csv_name[i])
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
        # case: custom pattern
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
                if res[len(res)-2] == "wrong":
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
    
    sys.stdout.write(json.dumps(result))
    
if __name__ == '__main__':
    django_data = input()
    json_data = json.loads(django_data)
    run = main(json_data)
    