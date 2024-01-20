from django.db import models

# Create your models here.
class Person(models.Model):
    student_id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    student_type = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return str(self.student_id) + " " + self.name + " " + str(self.surname)
    
class TestControl(models.Model):
    student_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=100, blank=True, null=True)
    # number of buttons to show in each level
    start_number_of_keys = models.IntegerField(blank=True, null = True)
    end_number_of_keys = models.IntegerField(blank=True,null = True)
    row_number = models.CharField(max_length=20, blank=True, null = True)
    column_number = models.CharField(max_length=20, blank=True, null = True)
    color = models.CharField(max_length=10, blank=True, null = True)    
    # number of trials per level
    trials = models.IntegerField(blank=True, null = True)
    csv_name = models.CharField(max_length=200, blank=True, null = True)
    csv_random_number = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return str(self.student_id) + ", test id = " + str(self.id)
        # return str(self.id)

class TestResult(models.Model):
    test_id = models.ForeignKey(TestControl, on_delete=models.CASCADE)
    # test_id = models.IntegerField(TestControl.id)
    number_of_keys = models.IntegerField(blank=True, null = True)
    pattern = models.TextField(blank=True, null = True)
    trials = models.IntegerField(blank=True, null = True)
    time_use = models.FloatField(blank=True, null = True)
    status = models.CharField(max_length = 100, blank=True, null = True)
    csv_name = models.TextField(default="-" ,blank=True, null = True)
    time_per_button = models.TextField(blank=True, null = True)
    
    def __str__(self):
        return str(self.test_id) + ", key = " + str(self.number_of_keys) + ", trial = " + str(self.trials) + ", time use = " + str(self.time_use)

class CSVFile(models.Model):
    # file = models.FileField(upload_to='myapp/media/file')
    file = models.FileField(upload_to='file/')
    # file_path = models.CharField(max_length=200, null=True)
    # date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return str(self.file)

class CSVFilePath(models.Model):
    file_path = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return str(self.file_path)