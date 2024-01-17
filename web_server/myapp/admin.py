from django.contrib import admin
from myapp.models import Person

# Register your models here.
admin.site.register(Person)

from myapp.models import TestControl
admin.site.register(TestControl)

from myapp.models import TestResult
admin.site.register(TestResult)

from myapp.models import CSVFile
admin.site.register(CSVFile)

from myapp.models import CSVFilePath
admin.site.register(CSVFilePath)