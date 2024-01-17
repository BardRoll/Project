from django.shortcuts import render, redirect
from myapp.models import Person
from myapp.models import RandomTestControl
from myapp.models import TestControl
from myapp.models import TestResult
from myapp.models import CSVFile
from myapp.models import CSVFilePath
from myapp.forms import CSVFileForm
from django.contrib import messages
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout

# Create your views here.
def sign_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            request, 
            username=username, 
            password=password
        )

        if user is not None:
            # Log user in
            login(request, user)
            return redirect('/')
        
        # return error message
        messages.error(request, 'Invalid login')
        
    return render(request, 'sign-in.html')

def sign_out(request):
    # sign user out
    logout(request)

    # Redirect to sign-in page
    # return redirect('/sign-in')
    return redirect('/')

def home(request):
    all_person = Person.objects.all()
    return render(request, "home.html", {"all_person":all_person})

@login_required(login_url="/sign-in")
def user_management(request):
    all_person = Person.objects.all()
    return render(request, "user_management.html", {"all_person":all_person})

@login_required(login_url="/sign-in")
def add_user(request):
    if request.method == "POST":
        # รับข้อมูล
        student_id = request.POST["student_id"]
        if Person.objects.exists():
            persons = Person.objects.all()
            for person in persons:
                if person.student_id == int(student_id):
                    messages.info(request,"Student id: " + str(student_id) + " has already been created!")
                    return render(request,"add_user.html")
        name = request.POST["name"]
        surname = request.POST["surname"]
        student_type = request.POST["student_type"]
        if "sports_type" in request.POST:
            student_type = request.POST["sports_type"]
        
        # บันทึกข้อมูล        
        person = Person.objects.create(
            student_id = student_id,
            name = name,
            surname = surname,
            student_type = student_type
        )
        person.save()
        messages.success(request,"Successfully saved")
        # เปลี่ยนเส้นทาง
        return redirect("/")        
    else :
        return render(request,"add_user.html")

@login_required(login_url="/sign-in")    
def edit_user(request, student_id):
    if request.method == "POST":
        person = Person.objects.get(student_id=student_id)
        person.student_id = request.POST["student_id"]
        person.name = request.POST["name"]
        person.surname = request.POST["surname"]
        person.student_type = request.POST["student_type"]
        person.save()
        messages.success(request,"Successfully updated")
        return redirect("/")  
    else:
        # ดึงข้อมูลที่ต้องการแก้ไข
        person = Person.objects.get(student_id=student_id)
        return render(request, "edit_user.html", {"person":person})
    
@login_required(login_url="/sign-in")
def delete_user(request, student_id):
    person = Person.objects.get(student_id=student_id)
    person.delete()
    messages.success(request,"Successfully deleted")
    return redirect("/")

@login_required(login_url="/sign-in")
def control_pattern(request, student_id):
    if request.method == "POST":
        person = Person.objects.get(student_id=student_id)        
        # student_id = person.student_id
        # level = request.POST["level"]
        # if request.POST["random"] is not None:
        #     random = request.POST["random"]
        # round = request.POST["round"]
        # if request.POST["file"] is not None:
        #     csv_name = request.POST["file"]
        # print(name, surname)
        # บันทึกข้อมูล
        # rtc = RandomTestControl.objects.create(
        #     student_id = student_id,
        #     level = level,
        #     random = random,
        #     round = round,
        #     csv_name = csv_name
        # )
        # create_row = RandomTestControl.objects.create(
        #     student_id = student_id
        # )
        # create_row.save()
        rtc = RandomTestControl()
        rtc.student_id = person
        if "level" in request.POST:
            rtc.level = request.POST["level"]
        if "random" in request.POST:
            rtc.random = request.POST["random"]
        if "round" in request.POST:
            rtc.round = request.POST["round"]
        if "file" in request.POST:
            rtc.csv_name = request.POST["file"]
        
        # print("level = ",rtc.level == '0')
        # print("round = ",rtc.round == '0')
        # print("random = ", "random" not in request.POST)
        # print("file1 = ", "file" not in request.POST)
        
        # Handle case
        # case 1. not select any options
        if rtc.level == '0' and rtc.round == '0' and "random" not in request.POST and "file" not in request.POST:
            messages.info(request,'Please select control')
            files = CSVFile.objects.all()
            # print("case1")
            return render(request, "control.html", {"person":person, 'files':files})
        
        # case 2. select only level or round ex:level=1, round=0 and select minus integer
        if (rtc.level <= '0' or rtc.round <= '0') and "random" not in request.POST and "file" not in request.POST:
            messages.info(request,'Level and Round must be greater than 0')
            files = CSVFile.objects.all()
            # print("case2")
            return render(request, "control.html", {"person":person, 'files':files})
        
        # case 3. select more than one option
        if ((rtc.level != '0' or rtc.round != '0') and "random" in request.POST and "file" in request.POST) or ((rtc.level != '0' or rtc.round != '0') and ("random" in request.POST or "file" in request.POST)) or ("random" in request.POST and "file" in request.POST):
            messages.info(request,'Select only one option')
            files = CSVFile.objects.all()
            print("case3")
            return render(request, "control.html", {"person":person, 'files':files})
        # level = str(person.level)
        rtc.save()
        
        # test = show_pattern()
        # for i in range(0,2):
        #     show_pattern().show_pattern_all(level)
        # test.show_pattern_all(level)
        messages.success(request,"Successfully controled")
        return redirect("/")  
    else:
        # ดึงข้อมูลที่ต้องการแก้ไข
        person = Person.objects.get(student_id=student_id)
        files = CSVFile.objects.all()
        return render(request, "control.html", {"person":person, 'files':files})

import subprocess
from django.http import HttpResponse
import json
import random
@login_required(login_url="/sign-in")
def custom_test_control(request, student_id):
    if request.method == "POST":
        person = Person.objects.get(student_id=student_id)
        tc = TestControl()
        tc.student_id = person
        tc.test_name = request.POST["test_name"]
        tc.start_number_of_keys = request.POST["start_key"]
        tc.end_number_of_keys = request.POST["end_key"]
        tc.row_number = request.POST["row"]
        tc.column_number = request.POST["column"]
        tc.color = request.POST["color"]
        tc.trials = request.POST["trial"]
        tc.csv_name = request.POST["file"]
        if tc.csv_name == "random":
            tc.csv_random_number = int(request.POST["random_number"])
            files = CSVFile.objects.all()
            file_list = [] # add file path to list
            for file in files:
                file_list.append(file.file.name)
            len_file_list = len(file_list) # for check random number
            if tc.csv_random_number > len_file_list:
                messages.info(request,'There are only ' + str(len_file_list) + ' CSV files')
                return render(request, "test_control.html", {"person":person, 'files':files})
            file_random = []
            for num in range(0, tc.csv_random_number):
                file_name_random = random.choice(file_list)
                file_random.append(file_name_random)
                file_list.remove(file_name_random)
            data_list = [tc.start_number_of_keys, tc.end_number_of_keys, tc.row_number, tc.column_number, tc.color, tc.trials, file_random]
        else:
            data_list = [tc.start_number_of_keys, tc.end_number_of_keys, tc.row_number, tc.column_number, tc.color, tc.trials, [tc.csv_name]]
        # print(tc.csv_name)
        tc.save()
        import os
        from django.conf import settings
        BASE_DIR = settings.BASE_DIR
        show_path = os.path.join(BASE_DIR, '..','show.py')
        python_path = os.path.join(BASE_DIR, '..','.venv', 'Scripts', 'python.exe')
        # send data to show.py
        # data_list = [tc.start_number_of_keys, tc.end_number_of_keys, tc.row_number, tc.column_number, tc.color, tc.trials, [tc.csv_name]]        
        data_to_send = json.dumps(data_list)
        # result = subprocess.run([r"D:\66\1\ProjectPrep\Launchpad\.venv\Scripts\python.exe", "-u", r"D:\66\1\ProjectPrep\Launchpad\show.py"], input=data_to_send, capture_output=True, text=True)
        result = subprocess.run([python_path, "-u", show_path], input=data_to_send, capture_output=True, text=True)
        # print("Wooooo")
        output_from_show_py = result.stdout
        # print("here1", result)
        # print("here2",output_from_show_py)
        output_json = json.loads(output_from_show_py)
        # print("here3 = ", type(output_json))
        
        # save output from show.py to TestResult
        len_output = len(output_json)
        if tc.csv_name == "-":
            for i in range(0, len_output):
                len_output_i = len(output_json[i])
                for j in range(0, len_output_i): # ถ้าผิดก่อนครบ trial ต้อง???
                    tr = TestResult()
                    tr.test_id= tc
                    tr.number_of_keys = int(output_json[i][j][0])
                    tr.pattern = output_json[i][j][1]
                    tr.trials = int(output_json[i][j][2])
                    tr.time_per_button = output_json[i][j][3]
                    tr.time_use = float(output_json[i][j][4])
                    tr.status = output_json[i][j][5]
                    tr.save()
        else:
            for i in range(0, len_output):
                len_output_i = len(output_json[i])
                for j in range(0, len_output_i):
                    tr = TestResult()
                    tr.test_id= tc
                    tr.number_of_keys = int(output_json[i][j][0])
                    tr.pattern = output_json[i][j][1]
                    tr.trials = int(output_json[i][j][2])
                    tr.time_per_button = output_json[i][j][3]
                    tr.time_use = float(output_json[i][j][4])
                    tr.status = output_json[i][j][5]
                    tr.csv_name = output_json[i][j][6]
                    tr.save()
        messages.success(request,"Successfully controled, test: " + str(tc.test_name))
        files = CSVFile.objects.all()
        return render(request, "test_control.html", {"person":person, 'files':files})
    else:
        # ดึงข้อมูลที่ต้องการแก้ไข
        person = Person.objects.get(student_id=student_id)
        files = CSVFile.objects.all()
        return render(request, "test_control.html", {"person":person, 'files':files})
    
@login_required(login_url="/sign-in")
def upload_csv(request):
    if request.method == 'POST':
        form = CSVFileForm(request.POST, request.FILES)
        # print(form.label_suffix.endswith('csv'))
        # if not form.label_suffix.endswith('csv'):
        #     messages.info(request,'Please Upload the CSV File only')
        #     # messages.success(request,'Please Upload the CSV File only')
        #     files = CSVFile.objects.all()
        #     return render(request, 'upload_csv.html', {'form': form, 'files': files})
        if form.is_valid():
            uploaded_file_path = str(form.instance.file.path)
            # index = uploaded_file_path.find('web_server')
            # new_uploaded_file_path = "myapp\media\file"+uploaded_file_path[index+10:]
            # print("upload = ",new_uploaded_file_path)
            # print("here ",new_uploaded_file_path)
            
            # csv_file = CSVFile.objects.all()
            # print(csv_file.file)
            form.save()
            csv_path = CSVFilePath.objects.create(file_path=uploaded_file_path)
            csv_path.save()
            # files = CSVFile.objects.all()
            # print("path ", files)

            # Process the uploaded CSV file (example: read using pandas)
            # csv_file = pd.read_csv(form.instance.file.path)
            # Perform further processing as needed
            
            # print(file_path.file_path.name)

            messages.success(request,"Successfully upload CSV")
            files = CSVFile.objects.all()
            return render(request, 'upload_csv.html', {'form': form, 'files': files})
        else:
            messages.info(request,'Please Upload the CSV File only')
    else:
        form = CSVFileForm()
        files = CSVFile.objects.all()
        # print("path ", files)
        # for i in files:
        #     print(i.file.name)
        # csv_file = CSVFile.objects.get(file= "myapp/csv_files/test_csv.csv")
        # filess = CSVFile.objects.get()
        # uploaded_file_path = form.instance.file.path
        # print(uploaded_file_path)
        # filename = request.FILES['file'].name
    
        return render(request, 'upload_csv.html', {'form': form, 'files': files})

import subprocess
from django.http import HttpResponse
import json
def run_show_py(request):
    data_list = ["2", "3", "4", "random", "multi", "2", "-"]
    # ส่งข้อมูลที่ต้องการไปยัง show.py (เปลี่ยนตามความต้องการของคุณ)
    data_to_send = json.dumps(data_list)
    import os
    from django.conf import settings
    BASE_DIR = settings.BASE_DIR
    APP_DIR = os.path.join(BASE_DIR, '..','show.py')
    full_path = os.path.join(BASE_DIR, '..','.venv', 'Scripts', 'python.exe')

    # เรียกใช้ show.py โดยใช้ subprocess
    # subprocess.run("&", "'d:/66/1/Project Prep/Launchpad/.venv/Scripts/Activate.ps1'")
    ##################
    result = subprocess.run([full_path, "-u", APP_DIR], input=data_to_send, capture_output=True, text=True)
    ##################
    # command = r"D:\66\1\ProjectPrep\Launchpad\.venv\Scripts\Activate.ps1 && python -u D:\66\1\ProjectPrep\Launchpad\show.py"
    # result = subprocess.run(command, input=data_to_send, shell=True, capture_output=True, text=True)
    # print("Wait...")
    # แสดงผลลัพธ์ที่ได้จาก show.py
    output_from_show_py = result.stdout
    print("here1", result)
    print("here",output_from_show_py)
    
    # start_index = output_from_show_py.find('{')
    # json_string = output_from_show_py[start_index:]
    # output_json = json.loads(json_string)
    # output = output_json["time_use"]
    
    # output_json = json.loads(output_from_show_py)


    # ส่งข้อมูลที่ได้จาก show.py กลับไปยังผู้ใช้
    # return HttpResponse(f"Output from show.py: {output_json}")
    
    ######################################################
    # person = Person.objects.get(student_id=6310000001)
    # tcs = TestControl.objects.filter(student_id=person)
    # return_dict = {}
    # id_na = 14
    # for tc in tcs:
    #     ress = TestResult.objects.filter(test_id=tc)
    #     for res in ress:
    #         if res.number_of_keys not in return_dict and tc.id == id_na:
    #             return_dict[res.number_of_keys] = {'id':tc.id, 'time_1':res.time_use, 'time_2':'-', 'best_time':res.time_use}
    #         else:
    #             if tc.id != id_na:
    #                 print('here')
    #                 continue
    #             return_dict[res.number_of_keys]['time_2'] = res.time_use
    #             if res.time_use < return_dict[res.number_of_keys]['best_time']:
    #                 return_dict[res.number_of_keys]['best_time'] = res.time_use
    ######################################################
    # for tc in tcs:
    #     ress = TestResult.objects.filter(test_id=tc)
    #     for res in ress:
    #         if tc.id not in return_dict:
    #             return_dict[tc.id] = {'key':res.number_of_keys, 'time_1':res.time_use, 'time_2':None, 'best_time':res.time_use}
    #         else:
    #             return_dict[res.number_of_keys]['time_2'] = res.time_use
    #             if res.time_use < return_dict[res.number_of_keys]['best_time']:
    #                 return_dict[res.number_of_keys]['best_time'] = res.time_use
    # print(type(tc.student_id))
    ######################################################
    # persons = Person.objects.all()
    # return_dict = {}
    # for person in persons:
    #     tcs = TestControl.objects.filter(student_id=person)
    #     person_id = person.student_id
    #     person_name = person.name
    #     for tc in tcs:
    #         ress = TestResult.objects.filter(test_id=tc)            
    #         for res in ress:
    #             if tc.id not in return_dict:
    #                 return_dict[tc.id] = {'student_id':person_id, 'student_name':person_name, 'id':tc.id, 'max_key':res.number_of_keys, 'time':res.time_use}
    #             else:
    #                 if res.number_of_keys > return_dict[tc.id]['max_key']:
    #                     return_dict[tc.id]['max_key'] = res.number_of_keys
    #                     if res.time_use < return_dict[tc.id]['time']:
    #                         return_dict[tc.id]['time'] = res.time_use
    
    return HttpResponse(f"Output from show.py: {APP_DIR}")

def test_result(request, student_id):
    ######################################################
    # person = Person.objects.get(student_id=student_id)
    # tcs = TestControl.objects.filter(student_id=student_id)
    # all_result = []
    # for tc in tcs:
    #     result = TestResult.objects.filter(test_id=tc)
    #     if result.exists():
    #         all_result.extend(result)
    # all_result = TestResult.objects.filter(test_id=tc)
    # print(all_result[0].number_of_keys)
    # print(tcs.id)
    # return render(request, "test_result.html", {"all_result":all_result, "person":person})
    ######################################################
    if request.method == 'POST':
        person = Person.objects.get(student_id=student_id)
        tcss = TestControl.objects.filter(student_id=person)
        return_dict = {}
        tcs = {}
        test_name = request.POST["test_name"]
        for tc in tcss:
            if tc.id not in tcs and tc.student_id == person:
                tcs[tc.id] = tc.test_name
            ress = TestResult.objects.filter(test_id=tc)
            for res in ress:
                # print("#########")
                # print(tc.test_name, " ", test_name)
                # print("#########")
                if res.number_of_keys not in return_dict and tc.test_name == test_name:
                    # print("yes")
                    return_dict[res.number_of_keys] = {'id':tc.test_name, 'time_1':res.time_use, 'time_2':'-', 'best_time':res.time_use, 'but_timestamp_1':res.time_per_button, 'but_timestamp_2':"-"}
                else:
                    if tc.test_name != test_name:
                        continue
                    return_dict[res.number_of_keys]['time_2'] = res.time_use
                    return_dict[res.number_of_keys]['but_timestamp_2'] = res.time_per_button
                    if res.time_use < return_dict[res.number_of_keys]['best_time'] and res.status == "pass":
                        return_dict[res.number_of_keys]['best_time'] = res.time_use
        # print(return_dict)
        return render(request, "test_result.html", {"all_result":return_dict, "person":person, "test_control":tcs, "test_name":{test_name:test_name}})
    else:
        person = Person.objects.get(student_id=student_id)
        tcss = TestControl.objects.all()
        tcs = {}
        for tc in tcss:
            if tc.id not in tcs and tc.student_id == person:
                tcs[tc.id] = tc.test_name
        # print(tcs)
        return render(request, "test_result.html", {"person":person, "test_control":tcs})
    
def test_result_all(request):
    persons = Person.objects.all()
    return_dict = {}
    for person in persons:
        tcs = TestControl.objects.filter(student_id=person)
        person_id = person.student_id
        person_name = person.name
        for tc in tcs:
            ress = TestResult.objects.filter(test_id=tc)            
            for res in ress:
                if tc.id not in return_dict:
                    return_dict[tc.id] = {'student_id':person_id, 'student_name':person_name, 'id':tc.test_name, 'max_key':res.number_of_keys, 'time':res.time_use}
                else:
                    if res.number_of_keys > return_dict[tc.id]['max_key'] and res.status == "pass":
                        return_dict[tc.id]['max_key'] = res.number_of_keys
                        return_dict[tc.id]['time'] = res.time_use
                    # need status = "pass" to show time used, 
                    elif res.number_of_keys == return_dict[tc.id]['max_key'] and res.time_use < return_dict[tc.id]['time'] and res.status == "pass":
                        return_dict[tc.id]['time'] = res.time_use
    
    return render(request, "test_result_all.html", {"all_result":return_dict})

# import csv

# def download_csv(request):
#     # ดึงข้อมูลจาก Django ที่ต้องการให้ผู้ใช้ดาวน์โหลด
#     data = TestResult.objects.all()

#     # สร้าง HttpResponse สำหรับ CSV
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="test_result_all.csv"'

#     # ใช้ csv.writer เพื่อเขียนข้อมูลลงใน HttpResponse
#     writer = csv.writer(response)
#     writer.writerow(['Header1', 'Header2', 'Header3'])  # เพิ่มหัวข้อที่ต้องการใน CSV

#     for row in data:
#         writer.writerow([row.field1, row.field2, row.field3])  # เพิ่มข้อมูลจากแต่ละแถว

#     return response