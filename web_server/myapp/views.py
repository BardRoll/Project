from django.shortcuts import render, redirect
from myapp.models import Person
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
        if request.POST["sports_type"] != "":
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
        tc.save()
        import os
        from django.conf import settings
        BASE_DIR = settings.BASE_DIR
        show_path = os.path.join(BASE_DIR, '..','show.py')
        python_path = os.path.join(BASE_DIR, '..','.venv', 'Scripts', 'python.exe')
        # send data to show.py     
        data_to_send = json.dumps(data_list)
        # result = subprocess.run([r"D:\66\1\ProjectPrep\Launchpad\.venv\Scripts\python.exe", "-u", r"D:\66\1\ProjectPrep\Launchpad\show.py"], input=data_to_send, capture_output=True, text=True)
        result = subprocess.run([python_path, "-u", show_path], input=data_to_send, capture_output=True, text=True)
        output_from_show_py = result.stdout
        output_json = json.loads(output_from_show_py)
        
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
        if form.is_valid():
            uploaded_file_path = str(form.instance.file.path)
            form.save()
            csv_path = CSVFilePath.objects.create(file_path=uploaded_file_path)
            csv_path.save()

            messages.success(request,"Successfully upload CSV")
            files = CSVFile.objects.all()
            return render(request, 'upload_csv.html', {'form': form, 'files': files})
        else:
            messages.info(request,'Please Upload the CSV File only')
    else:
        form = CSVFileForm()
        files = CSVFile.objects.all()
    
        return render(request, 'upload_csv.html', {'form': form, 'files': files})

@login_required(login_url="/sign-in")
def test_result(request, student_id):
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
                if res.number_of_keys not in return_dict and tc.test_name == test_name:
                    return_dict[res.number_of_keys] = {'id':tc.test_name, 'time_1':res.time_use, 'time_2':'-', 'best_time':res.time_use, 'but_timestamp_1':res.time_per_button, 'but_timestamp_2':"-"}
                else:
                    if tc.test_name != test_name:
                        continue
                    return_dict[res.number_of_keys]['time_2'] = res.time_use
                    return_dict[res.number_of_keys]['but_timestamp_2'] = res.time_per_button
                    if res.time_use < return_dict[res.number_of_keys]['best_time'] and res.status == "pass":
                        return_dict[res.number_of_keys]['best_time'] = res.time_use
        return render(request, "test_result.html", {"all_result":return_dict, "person":person, "test_control":tcs, "test_name":{test_name:test_name}})
    else:
        person = Person.objects.get(student_id=student_id)
        tcss = TestControl.objects.all()
        tcs = {}
        for tc in tcss:
            if tc.id not in tcs and tc.student_id == person:
                tcs[tc.id] = tc.test_name
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
